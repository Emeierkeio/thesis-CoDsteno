import requests
from bs4 import BeautifulSoup
from datetime import datetime
import utils


def main():
    """
    Scrapes the shorthand report of a parliamentary session from the Italian Chamber of Deputies website and creates a CSV file containing id_seduta, name of the deputies, argument and intervention text.

    Args:
        None.

    Returns:
        None.
    """
    for id in range(17, 187): # Modify the range to scrape different documents
        soup = get_html(id)
        createandsave_csv(soup, id)
        print("CSV file created for session {}".format(id))


def createandsave_csv(soup, id):
    """
    Creates and saves the CSV file containing id_seduta, name of the deputies, argument and intervention text.
    
    Args:
        soup: BeautifulSoup object.
        id: id_seduta.
        
    Returns:
        None.
    """

    session_date = get_sessiondate(soup)

    # Create the dictionary that links the id of the argument to the argument name
    argsdict = create_argsdict(soup)

    # create the list of interventions
    intervention_list = get_interventionlist(soup)

    # create the CSV file
    with open("19 Legislature sessions/session_{}.csv".format(id), "w") as csv_file:
        csv_file.write("id_seduta, session_date, deputy, governative_role, party, text, argument\n")

    for intervention in intervention_list:

        try:
            governative_role = intervention.em
        except:
            governative_role = ""
        
        try:
            party = intervention.span.text
        except:
            party = ""

        argument = get_argument(intervention["id"], argsdict)
        
        # Create a row of CSV file for each intervention
        row = ''
        row = row + str(id) + ', '
        row = row + str(session_date) + ', '
        row = row + utils.format_text(str(intervention.a)) + ', '
        row = row + utils.format_text(str(governative_role)) + ', '
        row = row + utils.format_text(str(party)) + ', '
        row = row + utils.format_text(str(intervention)) + ', '
        row = row + utils.format_text(str(argument))

        # Open a CSV file for writing
        with open("19 Legislature sessions/session_{}.csv".format(id), "a") as csv_file:
                
                # Write the row to the CSV file
                csv_file.write(row + "\n")



def get_argument(id, argsdict):
    """
    Gets the argument of the intervention from the id.
    
    Args:
        id: id of the intervention.
        argsdict: dictionary that links the id of the argument to the argument name.
        
    Returns:
    """

    splitted_args = id.split(".")
    # Find the arg that contains 'tit'
    for arg in splitted_args:
        if 'tit' in arg:
            break
    
    try:
        argument = argsdict[arg]
    except:
        print("Argument ID {} not found in dictionary".format(arg))
        argument = ""

    return argument


def get_interventionlist(soup):
    """
    Gets the list of interventions.

    Args:
        soup: BeautifulSoup object.
    
    Returns:
        intervention_list: list of interventions.
    """

    return soup.find_all("p", {"class": "intervento"})



def create_argsdict(soup):
    """
    Creates the dictionary that links the id of the argument to the argument name.
    
    Args:
        soup: BeautifulSoup object.
        
    Returns:
        argsdict: dictionary that links the id of the argument to the argument name.
    """

    argsdict = {}
    titoli = soup.find_all("p", {"class": "titolo"})

    for titolo in titoli:
        argid = titolo["id"].split(".")[-1]
        argsdict[argid] = titolo.strong

    return argsdict



def get_sessiondate(soup):
    """
    Gets the date of the session.

    Args:
        soup: BeautifulSoup object.
    Returns:
        data: date of the session.
    """

    # The date has the following format: "mercoledì 15 maggio 2022"
    data = soup.find_all("p", {"class": "centerBold"})[1].text
    day, month, year = data.split(' ')[-3:]
    day = day.replace('°', '')
    month = utils.months_itatoeng(month)
    data = datetime.strptime("{} {} {}".format(day, month, year), "%d %B %Y").strftime("%Y-%m-%d")
    return data
    


def get_html(id):
    """
    Gets the HTML of the shorthand report of the session.

    Args:
        id: id_seduta.

    Returns:
        soup: BeautifulSoup object.
    """  

    url = 'https://www.camera.it/leg19/410?idSeduta={}&tipo=stenografico' # 19 legislaure, change url for different legislatures
    print(url.format(id))
    response = requests.get(url.format(id))
    soup = BeautifulSoup(response.content.decode(), "html.parser")

    return soup    



if __name__ == '__main__':
    main()