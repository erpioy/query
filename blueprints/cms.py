from flask import Blueprint,render_template,redirect,g,jsonify,request,flash,url_for
from util.hooks import before_request
from models.user import PermissionEnum,UserModel,RoleModel
from util.decorators import permission_required
from forms.cms import AddStaffForm,EditStaffForm
from exts import db


bp = Blueprint("cms",__name__,url_prefix="/cms")

@bp.before_request
def cms_before_request():
    if not hasattr(g,"user") or g.user.is_staff == False:
        return redirect("/")
    
@bp.context_processor
def cms_context_processor():
    return {"PermissionEnum": PermissionEnum}


@bp.route('/index')
def cms_index():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template("/cms/staff_list.html",users=users)


@bp.route('/staff/list')
def staff_list():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template("/cms/staff_list.html",users=users)

@bp.route('/staff/add',methods=['GET','POST'])
@permission_required(PermissionEnum.CMS_USER)
def staff_add():
    form = AddStaffForm()
    if request.method == 'GET':
        roles = RoleModel.query.all()
        return render_template("cms/staff_add.html",roles=roles,form=form)
    else:
        if form.validate_on_submit():
            email = form.email.data
            role_id = form.role.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash('没有此用户')
                return redirect(url_for("cms.staff_list"))
            user.is_staff = True
            user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.staff_list"))
        
@bp.route('/staff/edit/<string:user_id>',methods=['GET','POST'])
def staff_edit(user_id):
    target_user = UserModel.query.get(user_id)
    form = EditStaffForm()
    if request.method == 'GET':
        roles = RoleModel.query.all()
        
        return render_template("cms/staff_edit.html",target_user=target_user,roles=roles,form=form)
    else:
        if form.validate_on_submit():
            is_staff = form.is_staff.data
            role_id = form.role.data
            target_user.is_staff = is_staff
            if target_user.role.id != role_id:
                target_user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.staff_edit",user_id=user_id))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("cms.staff_edit",user_id=user_id))
    
    



