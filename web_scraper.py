from http.cookiejar import CookieJar
import mechanicalsoup


def extract_challenge_title(page):
	node = page.find('div', { 'id': 'results_title' })
	return ''.join(node.find('span').findAll(text=True))


def extract_question_text(page):
	node = page.find('div', { 'class': 'question_challenge' })
	return ' '.join([text.strip() for text in node.findAll(text=True)])


def extract_solution_text(page):
	node = page.find('textarea')
	return node.contents


def create_difficulty_lookup(page):
	difficulty_lookup = {}
	for challenge in page.findAll('span', { "class": "each_challenge_tier1"}):
		title = ''.join(challenge.findAll(text=True)).strip()
		difficulty_lookup[title] = 'easy'

	for challenge in page.findAll('span', { "class": "each_challenge"}):
		title = ''.join(challenge.findAll(text=True)).strip()
		difficulty_lookup[title] = 'medium'

	for challenge in page.findAll('span', { "class": "each_challenge_tier3"}):
		title = ''.join(challenge.findAll(text=True)).strip()
		difficulty_lookup[title] = 'hard'

	return difficulty_lookup


def process_challenge_link(br, link):
	br.follow_link(link)
	root = br.get_current_page()
	# challenge_title = extract_challenge_title(root)
	# challenge_question = extract_question_text(root)
	solution_text = extract_solution_text(root)
	challenge_data = {
		"title": extract_challenge_title(root),
		"question_text": extract_question_text(root),
		"solution_text": extract_solution_text(root)
	}
	return challenge_data


def write_data_to_file(file_name, data):
	# if the file exists already then clear it out
	open(file_name, 'w').close()
	output = open(file_name, 'w', encoding='utf8')
	output.write(str(data))
	output.close()


def write_data_to_files(data):
	write_data_to_file('easy.json', data['easy'])
	write_data_to_file('medium.json', data['medium'])
	write_data_to_file('hard.json', data['hard'])
	write_data_to_file('none.json', data['none'])


def retrieve_challenges(login_username, password, profile_username):
	cj = CookieJar()
	br = mechanicalsoup.StatefulBrowser()
	br.set_cookiejar(cj)
	br.open("https://coderbyte.com/sl/")

	form = br.select_form(nr=1)
	form['username'] = login_username
	form['password'] = password
	br.submit_selected()

	br.open("https://coderbyte.com/profile/{}".format(profile_username))

	difficulty_lookup = create_difficulty_lookup(br.get_current_page())

	challenge_results = [process_challenge_link(br, link) for link in br.links(url_regex='^/results/')]

	results = {
		'easy': [],
		'medium': [],
		'hard': [],
		'none': []
	}
	for result in challenge_results:
		difficulty = difficulty_lookup.get(result['title'], 'none')
		results[difficulty].append(result)

	write_data_to_files(results)
