Liver, Potato Kotellets with Meat, 1 Apple	None	0	2023-12-23 13:48	Satiating, Full	None






{% if query.time_delta %}
    <td>{{ query.time_delta.seconds//3600 }} hours, {{ (query.time_delta.seconds//60)%60 }} minutes</td>
{% else %}
    <td>No time delta available</td>
{% endif %}



<td>{{query.time_delta}}</td>



{% if query.time_delta %}
    {% if query.time_delta.days == 0 %}
        <td>{{ query.time_delta.seconds//3600 }} hours, {{ (query.time_delta.seconds//60)%60 }} minutes</td>
    {% else %}
        <td>{{ query.time_delta.days }} days, {{ query.time_delta.seconds//3600 }} hours, {{ (query.time_delta.seconds//60)%60 }} minutes</td>
    {% endif %}
{% else %}
    <td>No time delta available</td>
{% endif %}




@app.route('/nutrition_index')
def nutrition_index():

    nutrition_query_all = eat.query.order_by(eat.date_added.asc()).all()


    return render_template('nutrition_index.html', nutrition_query_all=nutrition_query_all )



##### ADD NUTRITION 
## ADD FUnctionality to trigger   query_fasted_time ()
## IF It is the first record of today RUn the function.
@app.route('/add_nutrition/', methods = ['POST'])
def insert_nutrition():

    # Check if there are any records in the Eat model as of the current time
    # Create a subquery from the Select object
    #exists = db.session.query(eat.query.filter(cast(eat.date_added, Date) >= datetime.now().date())).exists()

    exists = db.session.query(
    db.session.query(eat).filter(cast(eat.date_added, Date) >= datetime.now().date()).exists()).scalar()

    if exists:
    # No need to trigger Fasting Time Calc function query_fasted_time ()
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
            return redirect(url_for('nutrition_index'))
        
    else: # Calculate Fasting Time
        
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
            flash("Fasting Time Calculated")
            query_fasted_time () # Calculate Fasting Time
        
        
            return redirect(url_for('nutrition_index'))
        



#### Delete Nutrition 
@app.route('/delete_nutrition/<int:id>', methods=['POST'])
def delete_nutrition(id):
    eat_to_delete = eat.query.get_or_404(id)
    db.session.delete(eat_to_delete)
    db.session.commit()
    return redirect(url_for('nutrition_index'))
    
<form action="{{ url_for('delete_nutrition', id=query.id) }}" method="POST">
                                <button type="submit" class="btn btn-danger">Delete</button>
                            </form>
         

        
       