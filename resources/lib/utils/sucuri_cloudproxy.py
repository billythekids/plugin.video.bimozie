import re, base64


class SucuriCloudProxy:
    @staticmethod
    def get_cookie(body):
        # get js cookie
        r = re.search("S='(.*)';L", body)
        code = base64.b64decode(r.group(1)).replace('\n', '').replace(" ", "")
        code = re.search(r'\w=(.*);document.cookie=(.*);location', code)

        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).substr\((\d),(\d)\)', r'\1[\2:\3]', code.group(1))
        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).slice\((\d),(\d)\)', r'\1[\2:\3]', a)
        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).charAt\((\d)\)', r'\1[\2]', a)
        a = re.sub(r'(String.fromCharCode\((\d+)\))', r"''.join(map(unichr, [\2]))", a)
        a = re.sub(r'(String.fromCharCode\((0x\d+)\))', r"''.join(map(unichr, [int(\2)]))", a)
        token = eval(a)

        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).substr\((\d),(\d)\)', r'\1[\2:\3]', code.group(2))
        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).slice\((\d),(\d)\)', r'\1[\2:\3]', a)
        a = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}|:;<>?]+[\'|"]).charAt\((\d)\)', r'\1[\2]', a)
        a = re.sub(r'(String.fromCharCode\((\d+)\))', r"''.join(map(unichr, [\2]))", a)
        a = re.sub(r'(String.fromCharCode\((0x\d+)\))', r"''.join(map(unichr, [int(\2)]))", a)
        a = re.sub(r'(\+\w\+)', "+token+", a)
        cookie_str = eval(a)

        list_cookie = {}
        cookies = cookie_str.split(';')
        for cookie in cookies:
            key, value = cookie.split('=')
            if 'path' not in key or 'max-age' not in key:
                list_cookie.update({key: value})

        return list_cookie


