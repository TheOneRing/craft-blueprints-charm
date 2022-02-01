from ctypes import util
import info
from Utils import CraftChoicePrompt

class subinfo(info.infoclass):
    def setTargets(self):
        platform = CraftCore.compiler.platform.name.lower()
        ext = "tar.gz"
        if CraftCore.compiler.isMacOS:
            platform = "Darwin"
        if CraftCore.compiler.isWindows:
            platform = "Windows"
            ext = "zip"
        for ver in ["0.7.0"]:
            self.targets[ver] = f"https://github.com/muesli/gitty/releases/download/v{ver}/gitty_{ver}_{platform}_x86_64.{ext}"
            self.targetInstallPath[ver] = "dev-utils/gitty"
            self.targetDigestUrls[ver] = (f"https://github.com/muesli/gitty/releases/download/v{ver}/checksums.txt", CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.7.0"

        self.description = "Contextual information about your git projects, right on the command-line"
        self.webpage = "https://github.com/muesli/gitty"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        env = {}
        kwargs = {}
        if "GITTY_TOKENS" not in os.environ:
            token = CraftChoicePrompt.promptForPassword(message='Enter the your gitty token', key="GITTY_TOKENS")
            env = {"GITTY_TOKENS" : token}
            kwargs["secret"] = [token]
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"gitty{CraftCore.compiler.executableSuffix}"),
                                os.path.join(self.imageDir(), "dev-utils", "gitty", f"gitty{CraftCore.compiler.executableSuffix}"), env=env, **kwargs)