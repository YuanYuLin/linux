import ops
import iopc

pkg_path = ""
output_dir = ""
tarball = ""
src_def_config = ""
dst_def_config = ""
build_dir = ""
initramfs_name = "initramfs.cpio.gz"
initramfs_file = ""
build_arch = ""
image_path = ""
image_output_name = "linux_image"

def set_global(args):
    global pkg_path
    global output_dir 
    global tarball
    global src_def_config
    global dst_def_config 
    global build_dir 
    global initramfs_file
    global build_arch
    global image_path
    pkg_args = args["pkg_args"]
    def_cfg_version = "default_" + pkg_args["version"] + ".config"
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    build_arch = ops.getEnv("ARCH")
    tarball = ops.path_join(pkg_path, "linux-4.3.tar.xz")
    build_dir = ops.path_join(output_dir, "linux-4.3")
    src_def_config = ops.path_join(pkg_path, def_cfg_version)
    if arch == "armel":
        image_path = "arch/arm/boot/zImage"
    elif arch == "x86_64":
        build_arch = "x86"
        image_path = "arch/x86/boot/bzImage"
    else:
        sys.exit(1)
    dst_def_config = ops.path_join(build_dir, ".config")
    initramfs_file = ops.path_join(iopc.getOutputRootDir(), initramfs_name)

def MAIN_ENV(args):
    set_global(args)

    return False

def MAIN_EXTRACT(args):
    set_global(args)
    ops.unTarXz(tarball, output_dir)
    #iopc.make_initramfs(iopc.getTargetRootfs(), iopc.getOutputRootFile(""))
    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(build_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    ops.kbuild_config_replace(src_def_config, dst_def_config, "CONFIG_INITRAMFS_SOURCE", initramfs_name)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.copyto(initramfs_file, build_dir)

    extra_conf = []
    extra_conf.append("ARCH=" + build_arch)
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("modules")
    extra_conf.append("ARCH=" + build_arch)
    iopc.make(build_dir, extra_conf)

    '''
    extra_conf = []
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("tarxz-pkg")
    iopc.make(build_dir, extra_conf)
    '''

    return False

def MAIN_INSTALL(args):
    set_global(args)

    ops.copyto(ops.path_join(build_dir, image_path), ops.path_join(iopc.getOutputRootDir(), image_output_name))
    '''
    extra_conf = []
    extra_conf.append("modules_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("firmware_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)
    '''
    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)
    print "linux kernel"

