from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

users = {
    'admin': {'password': 'admin123', 'role': 'admin', 'bio': 'Administrator', 'points': 0, 'profile_pic': None},
}

projects = [
    {'title': 'AI-powered Chatbot', 'team': 'Tech Titans', 'description': 'An AI chatbot that can answer student queries.', 'uploader': 'admin'},
    {'title': 'Smart Health Companion', 'team': 'Health Innovators', 'description': 'A device to manage medications and track health metrics.', 'uploader': 'admin'}
]

clubs = [
    {'name': 'Robotics Club', 'description': 'Building robots and competitions.', 'contact': 'robotics@dtc.com', 'members': ['admin'], 'events': []},
    {'name': 'Coding Club', 'description': 'Learn and develop coding skills.', 'contact': 'coding@dtc.com', 'members': ['admin'], 'events': []},
]

events = [
    {
        'id': 1,
        'name': 'CodeCraze Hackathon',
        'date': '2024-11-20',
        'description': 'A 48-hour hackathon for tech enthusiasts to develop innovative solutions.',
        'organizer': 'Delhi Tech Circuit',
        'category': 'Hackathon',
        'duration': '48 hours',
        'location': 'New Delhi, India',
        'price': 'Free',
        'capacity': 150,
        'tags': ['hackathon', 'AI', 'ML', 'cybersecurity'],
        'agenda': """
            Day 1: Opening Ceremony, Problem Statement Reveal, Hacking Begins.<br>
            Day 2: Mentorship Sessions, Workshops on AI, Cybersecurity.<br>
            Day 3: Project Submissions, Judging, Award Ceremony.
        """,
        'speakers': 'John Doe (AI Expert), Jane Smith (Cybersecurity Consultant)',
        'facilities': 'High-speed internet, 24-hour food and snacks, rest zones.',
        'prizes': 'Cash prizes, tech gadgets, internships with sponsor companies.',
        'details': """
            <strong>Hackathons:</strong> Teams compete to create tech solutions within a set time frame.<br>
            <strong>Workshops:</strong> Hands-on sessions on AI, web development, and cybersecurity led by industry experts.<br>
            <strong>Networking Sessions:</strong> Structured meet-and-greet opportunities for participants to connect with peers and mentors.<br>
            <strong>Panel Discussions:</strong> Talks on tech trends and career paths featuring industry leaders.<br>
            <strong>Tech Exhibitions:</strong> Clubs and startups showcase their projects and products with interactive demos.<br>
            <strong>Competitions:</strong> Coding challenges, quizzes, and design contests with prizes for winners.<br>
            <strong>Mentorship Programs:</strong> Pairing participants with mentors for guidance and advice.<br>
            <strong>Social Events:</strong> Informal gatherings and cultural programs to foster community spirit.<br>
            <strong>Feedback and Reflection:</strong> Sessions to share experiences and gather feedback for future improvements.
        """,
        'registered_users': [], 
        'number_of_registered_users': 0, 
        'max_users_allowed': 150  
    },
    {
        'id': 2,
        'name': 'Robotics Championship',
        'date': '2024-12-05',
        'description': 'A robotics competition showcasing cutting-edge robotic projects.',
        'organizer': 'Robotics Club',
        'category': 'Competition',
        'duration': '1 day',
        'location': 'Mumbai, India',
        'price': '₹500',
        'capacity': 100,
        'tags': ['robotics', 'competition', 'engineering'],
        'agenda': """
            Morning: Robotics Project Showcases.<br>
            Afternoon: Competition Rounds.<br>
            Evening: Prize Distribution and Networking.
        """,
        'speakers': 'Dr. Alan Walker (Robotics Researcher), Emily Wong (CEO, Robotech)',
        'facilities': 'Robotics Labs, Free Lunch, Networking Lounges.',
        'prizes': 'Robotics kits, cash rewards, and scholarships.',
        'details': """
            <strong>Event Format:</strong> Teams will showcase their robotics projects and compete in various challenges.<br>
            <strong>Workshops:</strong> Hands-on sessions on robotics programming and design.<br>
            <strong>Networking Opportunities:</strong> Meet with industry experts and fellow robotics enthusiasts.<br>
            <strong>Prizes:</strong> Attractive prizes for the winning teams.
        """,
        'registered_users': [],
        'number_of_registered_users': 0,
        'max_users_allowed': 100
    },
    {
        'id': 3,
        'name': 'Web Development Bootcamp',
        'date': '2024-12-15',
        'description': 'A hands-on bootcamp teaching modern web development technologies.',
        'organizer': 'Web Dev Club',
        'category': 'Workshop',
        'duration': '2 days',
        'location': 'Bangalore, India',
        'price': '₹1500',
        'capacity': 80,
        'tags': ['web development', 'HTML', 'CSS', 'JavaScript'],
        'agenda': """
            Day 1: Introduction to HTML, CSS, JavaScript.<br>
            Day 2: Hands-on Project: Building a Website.
        """,
        'speakers': 'Rahul Verma (Full Stack Developer), Priya Nair (UX/UI Expert)',
        'facilities': 'Free Wi-Fi, Certificate of Completion, Mentor Support.',
        'prizes': 'Best Project Award: Laptops and Tablets.',
        'details': """
            <strong>Workshop Overview:</strong> An interactive workshop to learn the basics of web development.<br>
            <strong>Hands-On Projects:</strong> Build your first website during the workshop.<br>
            <strong>Expert Guidance:</strong> Learn from experienced developers in the field.
        """,
        'registered_users': [],
        'number_of_registered_users': 0,
        'max_users_allowed': 80
    },
    {
        'id': 4,
        'name': 'AI & Machine Learning Summit',
        'date': '2024-01-10',
        'description': 'A conference exploring the latest advancements in AI and Machine Learning.',
        'organizer': 'AI Research Group',
        'category': 'Conference',
        'duration': '3 days',
        'location': 'Hyderabad, India',
        'price': '₹2000',
        'capacity': 300,
        'tags': ['AI', 'machine learning', 'data science'],
        'agenda': """
            Day 1: Keynote Speeches on AI Trends.<br>
            Day 2: Hands-on Workshops on ML Algorithms.<br>
            Day 3: Panel Discussions on AI Ethics and Future.
        """,
        'speakers': 'Dr. Neha Agarwal (AI Researcher), Dr. Ankit Mehta (ML Engineer)',
        'facilities': 'Conference Kits, Free Lunch and Coffee, Networking Events.',
        'prizes': 'Best Research Paper Award: ₹50,000 and job offers.',
        'details': """
            <strong>Keynote Speakers:</strong> Industry leaders share their insights on AI and machine learning trends.<br>
            <strong>Panel Discussions:</strong> Engage in discussions about the future of AI technologies.<br>
            <strong>Networking Sessions:</strong> Opportunities to connect with professionals and researchers in AI.
        """,
        'registered_users': [],
        'number_of_registered_users': 0,
        'max_users_allowed': 300
    },
    {
        'id': 5,
        'name': 'Cybersecurity Awareness Seminar',
        'date': '2024-01-20',
        'description': 'Learn about cybersecurity best practices and strategies to protect digital assets.',
        'organizer': 'Cybersecurity Club',
        'category': 'Seminar',
        'duration': '1 day',
        'location': 'Chennai, India',
        'price': 'Free',
        'capacity': 200,
        'tags': ['cybersecurity', 'data protection', 'hacking'],
        'agenda': """
            Morning: Introduction to Cybersecurity Threats.<br>
            Afternoon: Hands-on Simulation: Preventing Cyber Attacks.<br>
            Evening: Expert Panel on Future Cybersecurity Trends.
        """,
        'speakers': 'Alex Turner (Cybersecurity Expert), Sophie Lee (Ethical Hacker)',
        'facilities': 'Free Wi-Fi, Cybersecurity Tools Demos, Networking Lunch.',
        'prizes': 'Best Participant Award: Free Cybersecurity Certification.',
        'details': """
            <strong>Seminar Overview:</strong> Understand the importance of cybersecurity in today’s digital age.<br>
            <strong>Hands-On Sessions:</strong> Participate in simulations and learn about common security threats.<br>
            <strong>Expert Panel:</strong> Hear from cybersecurity experts about protecting your digital assets.
        """,
        'registered_users': [],
        'number_of_registered_users': 0,
        'max_users_allowed': 200
    }
]




newsfeed = [
    {'title': 'DTC Hackathon Registration Open!', 'date': '2024-10-11', 'content': 'Registrations are now open for the DTC Hackathon.'},
    {'title': 'Robotics Workshop Coming Soon', 'date': '2024-10-08', 'content': 'Build robots in this workshop by Robotics Club.'}
]

chat_messages = []
posts = []
post_id_counter = 1

# Upload directory for profile pictures and projects
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Intro route
@app.route('/')
def intro():
    return render_template('intro.html')

# User Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        bio = request.form.get('bio')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
        elif username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = {
                'password': password,
                'role': 'member',
                'bio': bio,
                'points': 0,
                'profile_pic': None
            }
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['bio'] = users[username].get('bio', '')
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = users[session['user']]
        user_events = [event for event in events if session['user'] in event['registered_users']]
        user_clubs = [club for club in clubs if session['user'] in club.get('members', [])]
        return render_template('dashboard.html', 
                               user=session['user'], 
                               profile_pic=user.get('profile_pic'),  
                               bio=user.get('bio', 'No bio provided.'), 
                               points=user.get('points', 0), 
                               events=user_events, 
                               clubs=user_clubs)
    return redirect(url_for('login'))



# Home page displaying events
@app.route('/event_calendar')
def event_calendar():
    return render_template('event_calendar.html', events=events)

# Event detail page
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        return render_template('event_detail.html', event=event)  # Ensure event is a dictionary
    return 'Event not found', 404

@app.route('/register/<int:event_id>', methods=['POST'])
def register(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        user = session['user']
        if user in event['registered_users']:
            # Unregister the user
            event['registered_users'].remove(user)
            event['number_of_registered_users'] -= 1
            flash(f'You have successfully unregistered from {event["name"]}!')
        else:
            # Register the user
            if event['number_of_registered_users'] < event['max_users_allowed']:
                event['registered_users'].append(user)
                event['number_of_registered_users'] += 1
                flash(f'Successfully registered for {event["name"]}!')
            else:
                flash('Registration failed: Event is full.')
    else:
        flash('Event not found.')
    return redirect(url_for('event_calendar'))



# Create a new event
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        new_event = {
            'id': len(events) + 1,
            'name': request.form['name'],
            'date': request.form['date'],
            'description': request.form['description'],
            'organizer': request.form['organizer'],
            'category': request.form['category'],
            'duration': request.form['duration'],
            'location': request.form['location'],
            'price': request.form['price'],
            'capacity': int(request.form['capacity']),
            'tags': request.form['tags'].split(','),
            'agenda': request.form['agenda'],
            'speakers': request.form['speakers'],
            'facilities': request.form['facilities'],
            'prizes': request.form['prizes'],
            'details': request.form['details'],
            'registered_users': [],
            'number_of_registered_users': 0,
            'max_users_allowed': int(request.form['capacity'])
        }
        events.append(new_event)
        flash('New event created successfully!')
        return redirect(url_for('event_calendar'))
    return render_template('create_event.html')

# Project Showcase and Upload
@app.route('/projects', methods=['GET', 'POST'])
def project_showcase():
    if request.method == 'POST':
        title = request.form['title']
        team = request.form['team']
        description = request.form['description']
        
        # Create the project dictionary without file handling
        projects.append({
            'title': title,
            'team': team,
            'description': description,
            'uploader': session['user']  # Save uploader's name
        })
        
        users[session['user']]['points'] += 20  # Add points for upload
        flash('Project uploaded successfully!', 'success')

        return redirect(url_for('project_showcase'))

    return render_template('projects.html', projects=projects)

@app.route('/project_upload', methods=['GET', 'POST'])
def project_upload():
    if request.method == 'POST':
        title = request.form['title']
        team = request.form['team']
        description = request.form['description']
        
        # Create the project dictionary without file handling
        projects.append({
            'title': title,
            'team': team,
            'description': description,
            'uploader': session['user']  # Save uploader's name
        })
        
        users[session['user']]['points'] += 20  # Add points for upload
        flash('Project uploaded successfully!', 'success')
        
        return redirect(url_for('project_showcase'))

    return render_template('project_upload.html')


# Clubs Directory
@app.route('/clubs', methods=['GET', 'POST'])
def clubs_directory():
    if request.method == 'POST':
        club_name = request.form.get('club_name')
        for club in clubs:
            if club['name'] == club_name and session['user'] not in club['members']:
                club['members'].append(session['user'])
                flash(f'You have successfully joined {club_name}!', 'success')
                return redirect(url_for('clubs_directory'))
        
    return render_template('clubs.html', clubs=clubs)

@app.route('/newsfeed', methods=['GET'])
def newsfeed_page():
    return render_template('newsfeed.html', newsfeed=newsfeed)

@app.route('/news_upload', methods=['GET', 'POST'])
def news_upload():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        newsfeed.append({
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        flash('News submitted successfully!', 'success')
        return redirect(url_for('newsfeed_page'))

    return render_template('news_upload.html')


# User Profile - Update Bio and Profile Picture
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            if profile_pic:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_pic.filename)
                profile_pic.save(file_path)
                users[session['user']]['profile_pic'] = profile_pic.filename

        bio = request.form.get('bio')
        users[session['user']]['bio'] = bio
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    user_info = users.get(session['user'])
    return render_template('profile.html', user=session['user'], profile_pic=user_info.get('profile_pic'), bio=user_info.get('bio'))

# Resource Library (Static)
@app.route('/resource_library')
def resource_library():
    resources = [
        {'title': 'Introduction to Python', 'link': 'https://www.learnpython.org/', 'description': 'Learn Python programming.'},
        {'title': 'Flask Documentation', 'link': 'https://flask.palletsprojects.com/', 'description': 'Flask web framework documentation.'}
    ]
    return render_template('resource_library.html', resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    global post_id_counter
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = session.get('username', 'Anonymous')

        if title and content:
            new_post = {
                'id': post_id_counter,
                'title': title,
                'content': content,
                'author': author,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'comments': []
            }
            posts.append(new_post)
            post_id_counter += 1
            flash('Post created successfully!', 'success')
            return redirect(url_for('forum'))
        else:
            flash('Please fill out all fields.', 'danger')

    return render_template('forum.html', posts=posts)

@app.route('/forum/post/<int:post_id>', methods=['POST'])
def post_comment(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        comment_content = request.form.get('comment')
        comment_author = session.get('username', 'Anonymous')
        if comment_content:
            comment = {
                'content': comment_content,
                'author': comment_author
            }
            post['comments'].append(comment)
            flash('Comment added successfully!', 'success')
        else:
            flash('Please fill out all fields for the comment.', 'danger')
    return redirect(url_for('forum'))

@app.route('/forum/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    flash('Post deleted successfully!', 'success')

    return redirect(url_for('forum'))

@app.route('/chat')
def chat():
    user = session.get('username', 'Guest')  # Get username from session
    return render_template('chat.html', user=user, chat_messages=chat_messages)


@socketio.on('send_message')
def handle_send_message(data):
    chat_messages.append({'user': data['user'], 'message': data['message']})
    emit('message', data, broadcast=True)  # Broadcast message to all users

@socketio.on('clear_chat')
def handle_clear_chat(user):
    # Clear only the current user's messages
    for message in chat_messages:
        if message['user'] == user:
            chat_messages.remove(message)
    emit('chat_cleared', user, broadcast=True)

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('intro'))



if __name__ == '__main__':
    socketio.run(app, debug=True)
