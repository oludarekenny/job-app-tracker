from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from werkzeug.utils import secure_filename

# ---------- Flask Setup ----------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# ---------- MySQL Connection ----------
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="dott",
        database="jobtracker",
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------- Initialize MySQL Table ----------
def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobApplications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_applied VARCHAR(50),
            company_name VARCHAR(255),
            role VARCHAR(255),
            application_source VARCHAR(255),
            cv_filename VARCHAR(255),
            stage1 VARCHAR(255),
            stage2 VARCHAR(255),
            stage3 VARCHAR(255),
            status VARCHAR(255),
            comments TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        file = request.files.get('cv')
        filename = None

        if file and file.filename.endswith(('.pdf', '.docx')):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = (
            request.form.get('date_applied', ''),
            request.form.get('company', ''),
            request.form.get('role', ''),
            request.form.get('source', ''),
            filename,
            request.form.get('stage1', ''),
            request.form.get('stage2', ''),
            request.form.get('stage3', ''),
            request.form.get('status', ''),
            request.form.get('comments', '')
        )

        conn = get_db()
        c = conn.cursor()

        c.execute("""
            INSERT INTO jobApplications
            (date_applied, company_name, role, application_source, cv_filename,
             stage1, stage2, stage3, status, comments)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)

        conn.commit()
        conn.close()

        return redirect(url_for('view_applications'))

    return render_template('form.html')


@app.route('/view')
def view_applications():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM jobApplications ORDER BY date_applied DESC")
    applications = c.fetchall()
    conn.close()

    return render_template('view.html', applications=applications)


@app.route('/delete/<int:app_id>', methods=['POST'])
def delete_application(app_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM jobApplications WHERE id=%s", (app_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_applications'))


@app.route('/update/<int:app_id>', methods=['GET', 'POST'])
def edit_application(app_id):
    conn = get_db()
    c = conn.cursor()

    if request.method == 'POST':
        file = request.files.get('cv')
        filename = request.form.get('existing_cv', '')

        if file and file.filename.lower().endswith(('.pdf', '.docx')):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = (
            request.form.get('date_applied', ''),
            request.form.get('company', ''),
            request.form.get('role', ''),
            request.form.get('source', ''),
            filename,
            request.form.get('stage1', ''),
            request.form.get('stage2', ''),
            request.form.get('stage3', ''),
            request.form.get('status', ''),
            request.form.get('comments', ''),
            app_id
        )

        c.execute("""
            UPDATE jobApplications
            SET date_applied=%s, company_name=%s, role=%s, application_source=%s,
                cv_filename=%s, stage1=%s, stage2=%s, stage3=%s, status=%s, comments=%s
            WHERE id=%s
        """, data)

        conn.commit()
        conn.close()
        return redirect(url_for('view_applications'))

    # GET — fetch record
    c.execute("SELECT * FROM jobApplications WHERE id=%s", (app_id,))
    app_data = c.fetchone()
    conn.close()

    return render_template('edit.html', app=app_data)


if __name__ == '__main__':
    app.run(debug=True)
