from app.extensions import logger


def decimal2str(decimal, count=2, prefix_plus=False, left=1, right=1):
    try:
        decimal = decimal / left
        decimal = decimal * right
    except Exception as e:
        logger.error(e)
    try:
        format_str = "%s%." + str(count) + "f"
        return format_str % ("+" if decimal > 0 and prefix_plus else "", decimal)
    except Exception as e:
        logger.error(e)
        return '-'
    pass


def decimal2unit(decimal, count=2):
    try:
        if not isinstance(decimal, float):
            decimal = float(decimal)
        decimal_unit = decimal / 10000 if decimal < 10000000 else decimal / 100000000
        unit = '万' if decimal < 10000000 else '亿'
        format_str = "%." + str(count) + "f%s"
        return format_str % (decimal_unit, unit)
    except Exception as e:
        logger.error(e)
        return '-'
    pass
