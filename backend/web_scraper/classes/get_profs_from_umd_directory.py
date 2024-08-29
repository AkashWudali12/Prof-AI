from human_request import HUMAN_REQUEST

class GET_PROFS_FROM_UMD_DIR:
    def __init__(self):
        self.faculty_listing = "https://faculty.eng.umd.edu/clark/facultydir?page=0&drfilter=5"

    def extract_profs_information(self):
        # Initialize lists to hold the extracted data
        names = []
        emails = []
        positions = []
        majors = []
        pictures = []

        num_pages = 27
        for i in range(num_pages):
            print("Page Number:", i + 1)
            self.faculty_listing = "https://faculty.eng.umd.edu/clark/facultydir?page=" + str(i) + "&drfilter=5"
            human_request = HUMAN_REQUEST(url=self.faculty_listing)
            soup = human_request.get_soup()

            # Loop through each faculty row
            for row in soup.find_all('div', class_='faculty_row'):
                # Extract name
                name_tag = row.find('div', class_='field-directory-name-title-wrapper').find('a')
                name = name_tag.get_text(strip=True) if name_tag else 'N/A'
                names.append(name)
                
                # Extract email
                email_tag = row.find('a', href=lambda x: x and x.startswith('mailto:'))
                email = email_tag.get_text(strip=True) if email_tag else 'N/A'
                emails.append(email)
                
                # Extract position
                position_tag = row.find('div', class_='title-wrapper').find('h3')
                position = position_tag.get_text(strip=True) if position_tag else 'N/A'
                positions.append(position)
                
                # Extract major
                major_tag = row.find('div', class_='field-directory-dept-contact-wrapper').find('a')
                major = major_tag.get_text(strip=True) if major_tag else 'N/A'
                majors.append(major)

                # Extract picture URL
                picture_tag = row.find('img', alt=True)
                picture_url = picture_tag['src'] if picture_tag else 'N/A'
                pictures.append(picture_url)

        # Combine the extracted data into a list of dictionaries
        faculty_data = [
            {"Name": name, "Email": email, "Position": position, "Major": major, "Picture URL": picture_url}
            for name, email, position, major, picture_url in zip(names, emails, positions, majors, pictures)
        ]

        return faculty_data
