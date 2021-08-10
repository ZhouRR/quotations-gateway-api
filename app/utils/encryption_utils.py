import base64
import binascii


def base64_encode(key):
    # base64编码：传入字节(或二进制)，最后返回字节
    b64_byt = base64.b64encode(key.encode('utf-8'))

    # 将字节转换成字符
    b64_str = b64_byt.decode('utf-8')
    return b64_str
    pass


def base64_decode(key):
    # base64解码：传入Base64编码后的字节或字符，最后返回字节
    try:
        byt = base64.b64decode(key)
    except binascii.Error as e:
        byt = None
        pass
    if byt is None:
        return ''
    # 将字节转换成字符
    try:
        rtn_str = byt.decode('utf-8')
        return rtn_str
    except UnicodeDecodeError as e:
        return None
    pass


if __name__ == '__main__':
    encode_equal_str = base64_encode("qw_qwerty").replace('=', 'equal')
    print(encode_equal_str)
    decode_str = base64_decode((encode_equal_str.replace('equal', '=')).encode('utf-8'))
    print(decode_str)
    encode_str = base64_encode("你过年干啥")
    print(encode_str)
    decode_str = base64_decode(encode_str.encode('utf-8'))
    print(decode_str)
    pass
