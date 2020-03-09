# -*- coding: utf-8 -*-
import re, base64


class SucuriCloudProxy:
    @staticmethod
    def get_cookie(body):
        # get js cookie
        r = re.search("S='(.*)';L", body)
        code = base64.b64decode(r.group(1)).replace('\n', '').replace(" ", "")
        code = re.search(r'\w=(.*);document\.cookie=(.*);[-\s]?location', code)
        token = eval(SucuriCloudProxy.parse(code.group(1)))
        a = SucuriCloudProxy.parse(code.group(2))
        a = re.sub(r'(\+\w\+)', "'"+token+"'", a)
        cookie_str = eval(a)

        print(cookie_str)
        list_cookie = {}
        cookies = cookie_str.split(';')
        for cookie in cookies:
            key, value = cookie.split('=')
            list_cookie.update({key: value})

        return list_cookie

    @staticmethod
    def parse(txt):
        txt = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}\|:;<>?\[\]=]+[\'|"]).substr\((\d),(\d)\)', r'\1[\2:\2+\3]', txt)
        txt = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}\|:;<>?\[\]=]+[\'|"]).slice\((\d),(\d)\)', r'\1[\2:\3]', txt)
        txt = re.sub(r'([\'|"][\w~`!@#$%^&*\(\)_-{}\|:;<>?\[\]=]+[\'|"]).charAt\((\d)\)', r'\1[\2]', txt)
        txt = re.sub(r'(String.fromCharCode\((\d+)\))', r"chr(\2)", txt)
        txt = re.sub(r'(String.fromCharCode\((0x\d+)\))', r"chr(int(\2))", txt)

        return txt
