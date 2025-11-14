
from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename 

#---flask App Setup -----

app = Flask(__name__) #--Initialize Flask app
app.config['UPLOAD_FOLDER'] = 'uploads' #directory where the uploaded cv's are saved
db_main= 'app_tracker.db' #sqlite db file

#initialize database
def init_db():
	with sqlite3.connect(db_main) as conn:
		c = conn.cursor()
		c.execute('''
            CREATE TABLE IF NOT EXISTS 	jobApplications (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				date_applied TEXT, 
				company_name TEXT, 
				role TEXT, 
				application_source TEXT, 
				cv_filename TEXT, 
				stage1 TEXT, 
				stage2 TEXT, 
				stage3 TEXT, 
				status TEXT, 
				comments TEXT
			)
			''')
	conn.commit()
  
init_db()


#Routes

@app.route('/', methods=['GET','POST'])
def form(): #define the form function
	if request.method == 'POST':
		file = request.files.get('cv')
		filename = None #initialize filename
  
  	#Allow for both PDF and Docx
  
		if file and file.filename.endswith(('.pdf','.docx')):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
				
			# Safely get all form data (empty strings if not filled)
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

		print("DEBUG: Data to insert:", data)  # Debug print

		# Insert into DB always
		with sqlite3.connect(db_main) as conn:
			c = conn.cursor()
			try:
				c.execute('''
					INSERT INTO jobApplications
					(date_applied, company_name, role, application_source, cv_filename, stage1, stage2, stage3, status, comments)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				''', data)
				conn.commit()
				print("DEBUG: Insert Successful")
			except Exception as e:
				print("DEBUG; DB error:", e)
     
		return redirect(url_for('view_applications'))

	return render_template('form.html')


#Route for the view page
@app.route('/view')
def view_applications():
    with sqlite3.connect(db_main) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM jobApplications ORDER BY date_applied DESC')
        applications = c.fetchall()
    return render_template('view.html', applications=applications)

#Route for the delete page
@app.route('/delete/<int:app_id>', methods=['POST'])
def delete_application(app_id):
    with sqlite3.connect(db_main) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM jobApplications WHERE id = ?', (app_id,))
        conn.commit()
    return redirect(url_for('view_applications'))

#update route
@app.route('/update/<int:app_id>', methods=['GET','POST'])
def edit_application(app_id):
    with sqlite3.connect(db_main) as conn:
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
        
        if request.method == 'POST':
            file = request.files.get('cv')
            filename = request.form.get('existing_cv', '')  # keep old if no new file
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

            c.execute('''
                UPDATE jobApplications
                SET date_applied=?, company_name=?, role=?, application_source=?, cv_filename=?,
                    stage1=?, stage2=?, stage3=?, status=?, comments=?
                WHERE id=?
            ''', data)
            conn.commit()
            return redirect(url_for('view_applications'))

        # GET request: fetch data to prefill form
        c.execute('SELECT * FROM jobApplications WHERE id=?', (app_id,))
        app_data = c.fetchone()

    return render_template('edit.html', app=app_data)

if __name__ == '__main__':
    app.run(debug=True)
                