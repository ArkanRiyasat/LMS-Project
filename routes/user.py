@user_bp.route('/profile')
@login_required
def profile():
    user = User.query.get_or_404(current_user.id)
    return render_template('user/profile.html', 
                         user={
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'username': user.username,
                             'email': user.email,
                             'phone': user.phone,
                             'role': user.role
                         })

from werkzeug.security import check_password_hash, generate_password_hash

@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    user = User.query.get_or_404(current_user.id)
    
    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('user.profile'))
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Password updated successfully', 'success')
    return redirect(url_for('user.profile'))