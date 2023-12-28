# College Basketball Model

This is a model that can predict a line of a college basketball game given three different sources of statistical data. 

## Using the Model

To recieve a line prediction from this model, there are a few steps that must be taken to set it up. Follow these instructions in order to properly use the model.

### Loading the Data

Data must be loaded manually before starting up the model. These three links are where the data must be retrieved from:

- [Sports Reference Advanced School Stats](https://www.sports-reference.com/cbb/seasons/men/2024-advanced-school-stats.html)
- [Sports Reference Advanced Opponent Stats](https://www.sports-reference.com/cbb/seasons/men/2024-advanced-opponent-stats.html)
- [Pomeroy College Basketball Ratings](https://kenpom.com)

For the first two, navigate to those links. Look for a button that says `Share & Export ▾`. Click that, followed by a link that says `Modify, Export, and Share Table`, and then press `comma-seperated`.

Copy that info and paste it into `sr-school-stats.csv` and `sr-opponent-stats.csv` respectively, overwritting what is already in there. Make sure to erase the extra spaces at the top so the line containing "Overall" is first.

For the Pomeroy College data, that link must be opened in Chrome, with the [Table Capture](https://chromewebstore.google.com/detail/table-capture/iebpjdmgckacbodjpijphcplhebcmeop) extension installed. Navigate to the Pomeroy College website, right click on the table, and hover over `Table Capture`. You should then see another two options appear, click on the one containing `Launch workshop`. Export the table as a CSV (if that doesn't work, try exporting it to google sheet and then downloading it as a CSV). Then paste all that data into `kenpom-stats.csv`, making sure there is no extra space before the first line.

The `hca.json` file represents home-court advantages. It is already populated with known advantages. If new discoveries are made, this can be easily updated. To add a new home-court advantage for a school, add a new entry to `schools`, with the name of the school formatted the same as in the Pomeroy College file. To add a new home-court advantage for a conference, do the same to the `conference` mapping, making sure the name is consistent with the Pomeroy College file. The model will know to grab an advantage from there.

Now that our data is properly loaded, we can run the model.

### Running the Model

In order to run the model and start the UI, execute the Python script, model.py, with the three data files as such (file order matters):

**Two important disclaimers:**
- You may have to replace the file names in the execution call if they are different in your local filesystem.
- If the execution call doesn't work, try replacing `python` with `python3`
```
python model.py sr-school-stats.csv sr-opponent-stats.csv kenpom-stats.csv
```
That should launch the model and start the interactive UI as such:
```
Hello, welcome to the model. To quit, type 'exit' for one of the team names
Choose home team: 
```
Go ahead and enter the name of the home team, as formatted in the Pomeroy College stats file. Do the same with the away team. Lets use Purdue (home), Houston (away), as an example.
```
Choose home team: Purdue
Choose home team: Houston
```
After pressing enter, your response should be:
```
Purdue (HOME) vs. Houston (AWAY)
The result is: +6.76
Continue or Exit?: 
```
From here, you can either exit by typing in "exit" (case doesn't matter), or continue by typing in anything else. Continue will restart the interative UI so you can query more matchups

At any point during input, if you type `exit`, the UI will close.