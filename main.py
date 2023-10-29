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
    for id in range(1, 187): # Modify the range to scrape different documents
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

    for intervention in intervention_list:

        intervention_description = intervention[0]

        try:
            governative_role = intervention_description.em
        except:
            governative_role = ""
        
        try:
            party = intervention_description.span.text
        except:
            party = ""

        argument = get_argument(intervention_description["id"], argsdict)
        
        # Create a row of CSV file for each intervention
        row = ''
        row = row + str(id) + ', '
        row = row + str(session_date) + ', '
        row = row + 'XIX' + ',' # 19 legislaure, change for different legislatures
        row = row + utils.format_text(str(intervention_description.a)) + ', '
        row = row + utils.format_text(str(governative_role)) + ', '
        row = row + utils.format_text(str(party)) + ', '
        row = row + utils.format_text(str(intervention)) + ', '
        row = row + utils.format_text(str(argument))

        # Open a CSV file for writing
        with open("data/sessions.csv".format(id), "a") as csv_file:
                
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

    try:
        if 'sub' in id.split(".")[-2]:
            argument = argsdict[".".join(id.split(".")[-3:-1])]
        else:
            argument = argsdict[id.split(".")[-2]]
    except:
        print("Error: argument not found for id {}".format(id.split(".")[-2]))
        argument = ""

    return argument


def get_interventionlist(soup):
    """
    Gets the list of interventions.
    TODO: Finora prendi solo la prima frase di ogni intervento!

    Args:
        soup: BeautifulSoup object.
    
    Returns:
        intervention_list: list of interventions.
    """
    paragraphs = soup.find_all("p")
    # find all the p of class interventoVirtuale after each p class intervento

    intervention_list = []
    intervention = []

    # This is necessary because there are a 'interventoVirtuale' for each sentences in the same intervento
    for paragraph in paragraphs:
        if paragraph.get('class') == ['intervento']:
            intervention_list.append(intervention)
            intervention = []
            intervention.append(paragraph)
        elif paragraph.get('class') == ['interventoVirtuale']:
            intervention.append(paragraph.text)
        else:
            pass
        
    return intervention_list[1:]



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
    titoli_allegati = soup.find_all("p", {"class": "titolo_allegato"})
    sottotitoli = soup.find_all("p", {"class": "sottotitolo"})

    for titolo in titoli:
        argid = titolo["id"].split(".")[-1]
        argsdict[argid] = titolo.strong

    for sottotitolo in sottotitoli:
        argid = ".".join(sottotitolo["id"].split(".")[-2:])
        argsdict[argid] = sottotitolo.strong

    for titolo_allegato in titoli_allegati:
        argid = titolo_allegato["id"].split(".")[-1]
        argsdict[argid] = titolo_allegato.strong

    # Add tit00000 for "interventi iniziali"
    argsdict['tit00000'] = 'Interventi iniziali'

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