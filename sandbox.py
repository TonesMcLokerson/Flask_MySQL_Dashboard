# Payroll
@app.route('/Payroll')
@is_logged_in
def payroll():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get Payroll
    result = cur.execute("SELECT * FROM payroll")

    Payroll = cur.fetchall()

    if result > 0:
        return render_template('payroll.html', payroll=payroll)
    else:
        msg = 'No Payroll Found'
        return render_template('payroll.html', msg=msg)
    # Close connection
    cur.close()

#Single Payroll
@app.route('/payroll/<string:pay_id>/')
def payroll(pay_id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get Payroll
    result = cur.execute("SELECT * FROM payroll WHERE pay_id = %s", [pay_id])

    payroll = cur.fetchone()

    return render_template('payroll.html', payroll=payroll)

# Payroll Form Class
class PayrollForm(Form):
	type = StringField( 'Type', [validators.Length(min=1, max=50)])
	payrate = StringField( 'Brand', [validators.Length(min=1, max=50)])
	 = StringField( 'Spend', [validators.Length(min=1, max=100)])

# Add Payroll
@app.route('/add_payroll', methods=['GET', 'POST'])
@is_logged_in
def add_payroll():
	form = ProgramForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		brand = form.brand.data
		spend = form.spend.data

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO payroll(name, brand, spend) VALUES(%s, %s, %s) ", (name, brand, spend))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("Payroll Successflly Uploaded", 'success')

		return redirect(url_for('payroll'))

	return render_template('add_payroll.html', form=form)
