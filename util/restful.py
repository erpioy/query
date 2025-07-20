from flask import jsonify


# @author xiaosu
# @since 2025-07-10

class HttpCode:
    """
        类属性，通过类名.属性名调用，全局共享唯一
    """
    # 响应正常
    OK = 200
    # 没有登录错误
    UNLOGINERROR = 401
    # 没有权限错误
    PERMISSIONERROR = 403
    # 客户端参数错误
    PARAMSERROR = 400
    # 服务器错误
    SERVERERROR = 500

def _restful_result(code,message,data):
    return jsonify({"message":message or "","data":data or {}}),code

def ok(message=None,data=None):
    return _restful_result(code=HttpCode.OK,message=message,data=data)

def unlogin_error(message="没有登录~"):
    return _restful_result(code=HttpCode.UNLOGINERROR,message=message,data=None)

def permission_error(message="没有权限访问~"):
    return _restful_result(code=HttpCode.PERMISSIONERROR,message=message,data=None)

def params_error(message="客户端参数错误"):
    return _restful_result(code=HttpCode.PARAMSERROR,message=message,data=None)

def server_error(message="服务器端错误"):
    return _restful_result(code=HttpCode.SERVERERROR,message=message,data=None)
