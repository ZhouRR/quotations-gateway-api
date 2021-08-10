import configparser


def config_get(config_path, section_name, *names):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    for name in names:
        yield conf.get(section_name, name)


def config_getint(config_path, section_name, *names):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    for name in names:
        yield conf.getint(section_name, name)


def config_getfloat(config_path, section_name, *names):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    for name in names:
        yield conf.getfloat(section_name, name)


def config_set(config_path, section_name, *values):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    if not conf.has_section(section_name):
        conf.add_section(section_name)
    for value in values:
        conf.set(section_name, value['name'], str(value['value']))
    conf.write(open(config_path, 'w'))


def config_rm(config_path, section_name, *names):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    for name in names:
        conf.remove_option(section_name, name)
    conf.write(open(config_path, 'w'))
    pass


def all_options(config_path, section_name):
    conf = configparser.ConfigParser()
    conf.optionxform = lambda option: option
    # 读取.ini文件
    conf.read(config_path)
    items = conf.items(section_name)
    return items, conf
    pass


def config_clean(config_path, section_name):
    items, conf = all_options(config_path, section_name)
    for item in items:
        conf.remove_option(section_name, item[0])
    conf.write(open(config_path, 'w'))
    pass
