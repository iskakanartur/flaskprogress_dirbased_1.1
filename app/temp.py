Liver, Potato Kotellets with Meat, 1 Apple	None	0	2023-12-23 13:48	Satiating, Full	None






##### ADD NUTRITION 
## ADD FUnctionality to trigger   query_fasted_time ()
## IF It is the first record of today RUn the function.
@app.route('/add_nutrition/', methods = ['POST'])
def insert_nutrition():
    if request.method =='POST':
        session = eat(
            meal =    request.form.get('meal'),
            drink =   request.form.get('drink'),
            drink_count =   request.form.get('drink_count'),
            date_added = request.form.get('date_added'),
            comment =    request.form.get('comment')
            

        )
        db.session.add(session)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")



        
        return redirect(url_for('nutrition_overview'))