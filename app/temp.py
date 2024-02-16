@app.route('/daily_fit_stats_viz')
def daily_fit_stats_viz():
  # SQLAlchemy query
    result = db.session.query(
    fit.exercise,
    func.trim(func.to_char(fit.date_added, 'Day')).label('day_of_week'),
    func.sum(fit.exercise_count).label('total_exercise_count')
    ).filter(
    and_(
        fit.date_added >= func.date_trunc('week', func.current_date()),
        fit.date_added <= func.now()
    )
    ).group_by(
        fit.exercise, 'day_of_week'
    ).order_by(
        fit.exercise, 'day_of_week'
    ).all()


    # Create a bar graph
    days_of_week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Dictionary to store aggregated data
    data = {exercise: {day: 0 for day in days_of_week_order} for exercise in set(row.exercise for row in result)}

    for row in result:
        data[row.exercise][row.day_of_week] = row.total_exercise_count

    # Plotting
    plt.figure(figsize=(10, 6))
    for exercise, counts in data.items():
        plt.bar(counts.keys(), counts.values(), label=exercise)

    plt.title("Exercise Count for Each Exercise on Each Day of the Week")
    plt.xlabel("Day of the Week")
    plt.ylabel("Total Exercise Count")
    plt.legend()

    # Convert the plot to HTML using mpld3
    plot_html = mpld3.fig_to_html(plt.gcf())

    


    return render_template('daily_fit_stats_viz.html', plot_html=plot_html)