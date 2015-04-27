import json
import requests
import xml.etree.ElementTree as ET

# This class implements a wrapper on the User Modeling service
class RelationshipExtraction:
    API_RELATIONSHIP = "https://gateway.watsonplatform.net/relationship-extraction-beta/api"
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _formatPOSTData(self, text):
        return {
            'txt': text,
            'sid': 'ie-en-news'
        }

    def extractRelationship(self, text):
        if self.API_RELATIONSHIP is None:
            raise Exception("No User Modeling service is bound to this app")
        payload = self._formatPOSTData(text)
        r = requests.post(self.API_RELATIONSHIP,
                          auth=(self.user, self.password),
                          headers={'content-type': 'application/json'},
                          params=payload
        )
        print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
        if r.status_code != 200:
            try:
                error = json.loads(r.text)
            except:
                raise Exception("API error, http status code %d" % r.status_code)
            raise Exception("API error %s: %s" % (error['error_code'], error['user_message']))
        return r.text
    def parseMentions(self,tree):
        types = {
            "Animal": {
                "roles": [
                    "PEOPLE",
                    "PERSON",
                    "PERSONPEOPLE"
                ],
                "subtypes": None
            },
            "AWARD": {
                "roles": [
                    "EVENT_PERFORMANCE",
                    "PERSON"
                ],
                "subtypes": None
            },
            "DISEASE": {
                "roles": None,
                "subtypes": None
            },
            "EVENT": {
                "roles": None,
                "subtypes": ["EVENT_AWARD", "EVENT_BUSINESS", "EVENT_DEMONSTRATION", "EVENT_ELECTION", "EVENT_PERFORMANCE",
                             "EVENT_SPORTS", "EVENT_VIOLENCE"]
            },
            "FACILITY": {
                "roles": ["ORGANIZATION"],
                "subtypes": None
            },
            "GPE": {
                "roles": ["ORGANIZATION"],
                "subtypes": [
                    "AREA",
                    "COUNTRY",
                    "UNSPECIFIED"
                ]
            },
            "IDEOLOGY": {
                "roles": None,
                "subtypes": None
            },
            "LAW": {
                "roles": None,
                "subtypes": None
            },
            "LOCATION": {
                "roles": None,
                "subtypes": None
            },
            "ORGANISATION": {
                "roles": None,
                "subtypes": [
                    "COMMERCIAL",
                    "EDUCATIONAL",
                    "GOVERNMENT",
                    "MILITARY",
                    "MULTIGOV",
                    "POLITICAL",
                    "RELIGIOUS",
                    "SPORTS"
                ]
            },
            "PERSON": {
                "roles": ["OCCUPATION"],
                "subtypes": None
            },
            "PRODUCT": {
                "roles": None,
                "subtypes": None
            },
            "TITLEWORK": {
                "roles": None,
                "subtypes": None
            },
            "VEHICLE": {
                "roles": ["PRODUCT", "WEAPON"],
                "subtypes": None
            },
            "WEAPON": {
                "roles": None,
                "subtypes": None
            }

        }

        nodes = []
        edges = []
        for child in types.keys():
            nodes.append({
                "id": child,
                "label": child,
                "shape": "circle",
                "group": child
            })

            edges.append({
                "from": "interests",
                "to": child
            })

        root = ET.fromstring(tree)
        for child in root[0][2]:
            if child.attrib["etype"] in types.keys() and child.attrib["score"] > 0.5 and child.attrib["mtype"] == "NAM":
                # print child.text + ": " + child.attrib["etype"]
                if not node_exist(child.text, nodes):
                    nodes.append({
                        "id": child.text.upper(),
                        "label": child.text,
                        "shape": "dot",
                        "group": child.attrib["etype"]
                    })
                    edges.append({
                        "from": child.attrib["etype"],
                        "to": child.text.upper()
                    })

        return nodes, edges

class PersonalityInsights:
    API_PERSONALITY = "https://gateway.watsonplatform.net/personality-insights/api"
    def __init__(self, user, password):
        self.user = user
        self.password = password


    def getProfile(self, text):


        response = requests.post(self.API_PERSONALITY + "/v2/profile",
                          auth=(self.user, self.password),
                          headers = {"content-type": "text/plain"},
                          data=text
                          )
        try:
            return json.loads(response.text)
        except:
            raise Exception("Error processing the request, HTTP: %d" % response.status_code)

    def flattenPortrait(self,tree):
        nodes = []
        edges = []

        def f(t):
            if t is None:
                return None
            # if level > 0 and (("children" not in t) or level != 2):
            if t["id"] == 'r':
                nodes.append({
                    "id": t["id"],
                    "label": "portrait",
                    "shape": "circle",
                    "value": 300
                })
            else:
                nodes.append({
                    "id": t["id"],
                    "label": t["name"] + "\n" + ("%d%%" % int(t["percentage"] * 100) if "percentage" in t else ""),
                    "group": t["category"] if "category" in t else "",
                    "shape": "dot",
                    "value": int(t["percentage"] * 100) if "percentage" in t else 100
                })
            if "children" in t:
                for elem in t["children"]:
                    if t["id"] != elem["id"]:
                        edges.append({
                            "from": t["id"],
                            "to": elem["id"]
                        })
                    f(elem)

        f(tree)
        return nodes, edges



def node_exist(targetId,nodes):
    exist= False
    for node in nodes:
        if targetId == node["id"]:
            exist=True
            break;
    return exist