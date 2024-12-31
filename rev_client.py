import json
from aiohttp import ClientConnectorError
import traceback
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup


class RevClient:
    def __init__(self, host, username, password, session):
        self.host = host
        self.username = username
        self.password = password
        self.__Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        self.__Session: aiohttp.ClientSession = session
        self.csrfToken = None

    async def login(self):
        try:
            async with self.__Session.get(url=self.host + "/login/signIn", 
                                          headers=self.__Headers,
                                          ssl=False) as resp:
                if resp.status != 200:
                    print(f"Failed to load login page. Status code: {resp.status}")
                    return False
                token_html = await resp.text()

            soup = BeautifulSoup(token_html, "html.parser")
            token_element = soup.find("input", attrs={"name": "csrfToken"})
            if not token_element:
                print("CSRF token not found in login page.")
                return False
            self.csrfToken = token_element["value"]

            login_form = aiohttp.FormData()
            login_form.add_field("csrfToken", self.csrfToken)
            login_form.add_field("username", self.username)
            login_form.add_field("password", self.password)
            login_form.add_field("source", "")
            login_form.add_field("remember", "1")

            async with self.__Session.post(
                url=self.host + "/login/signIn",
                data=login_form,
                headers=self.__Headers,
                ssl=False
            ) as resp:
                if resp.ok: return True
                if resp.status not in (200, 302):
                    print(f"Login failed. Status code: {resp.status}")
                    return f"Login failed. Status code: {resp.status}"

                if resp.status == 302 and resp.headers.get("Location"):
                    redirection_url = resp.headers.get("Location")
                    if redirection_url.endswith("/submissions"):
                        return True

                login_text = await resp.text()
                
                if "Salir" in login_text:
                    return True
                else:
                    print("Login response does not contain expected content.")
                    return ("Login response does not contain expected content.")
        except ClientConnectorError as e:
            print(f"Error de conexión: {e}")
            return f"Error de conexión: {e}"
        except Exception as ex:
            print(traceback.format_exc())
            print(f"Error in login: {ex}")
            return str(ex)


    async def upload(self, path: Path, repo_id: int):
        try:
            path = Path(path)
            if not path.exists() or not path.is_file():
                raise FileNotFoundError(f"File not found: {path}")

            with path.open("rb") as file:
                form = aiohttp.FormData()
                form.add_field("fileStage", "2")
                form.add_field("name[es_ES]", path.name)
                form.add_field("file", file, filename=path.name)

                async with self.__Session.post(url=f"{self.host}/api/v1/submissions/{repo_id}/files",
                                               data=form,
                                               headers={**self.__Headers,
                                                        "X-Csrf-Token": self.csrfToken},
                                               ssl=False) as resp:
                    try:
                        response = await resp.json()
                    except aiohttp.ContentTypeError:
                        response = json.loads(await resp.text())

                    return response.get("url", None)
        except ClientConnectorError as ex:
            print(f"Error de conexión: {ex}")
            return f"Error de conexión: {ex}"
        except Exception as ex:
            print(f"Error in upload: {ex}")
            return str(ex)
