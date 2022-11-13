from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

SEASON = 2022
SEASON_GAMES = []

def makerows(row):
    words = ""

    for i, letter in enumerate(row):
        if not letter.isdigit():
            words += letter
        else:
            return [words.strip(), *row[i:].split(" ")]

def main():
    file1 = open("myfile.txt","w")
    driver = webdriver.Edge()
    driver.get("https://fgcuathletics.com/sports/womens-soccer/stats/2022")
    assert "Page not found" not in driver.page_source
    

    for i in range(1, 5):
        selects = Select(driver.find_element(By.XPATH, "//select"))
        selects.select_by_index(i)
        driver.find_element(By.XPATH, "//li//a[contains (@id, 'ui-id-3')]").click()
        driver.find_element(By.XPATH, "//li//a[contains (@id, 'ui-id-12')]").click()
        table_rows = []

        table_data = driver.find_elements(By.XPATH, '//table[1]//thread//tr//th')
        table_rows.append([h.text for h in table_data if h.text])

        table_data = driver.find_elements(By.XPATH, '//table[1]//tbody//tr')
        for row in table_data:
            if row.text:
                cur_row = makerows(row.text)
                if cur_row is None or len(cur_row) == 1:
                    continue
                else:
                    table_rows.append(cur_row)
        
        for j, row in enumerate(table_rows):
            if (j == 0):
                print(f"{SEASON - i} stats")
                continue
            print(f"Row {j} is: {row}")
            file1.writelines(f"Row {j} is: {row}\n")
        SEASON_GAMES.append(len(table_rows) -1)
    
    for i in range(len(SEASON_GAMES)):
        print(f"Season {SEASON-i} had {SEASON_GAMES[i]} games")
        file1.writelines(f"Season {SEASON-i} had {SEASON_GAMES[i]} games")
    SEASON_GAMES.sort()
        
    driver.close()
    file1.close()


if __name__ == "__main__":
    main()