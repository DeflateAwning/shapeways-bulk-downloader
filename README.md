# shapeways-bulk-downloader
A tool to bulk download a big list of files from Shapeways

## Purpose
This tool downloads a list of files from Shapeways, based on the code in the links of the files. It also extracts those models.

## State
This tool works, and has been used by me to download 100 models. It is still a little rough around the edges though. If you have issues or would like to be easier to use, please open an Issue and I'll work to make it better.

## How to Use
1. Find the links to the Shapeways models you want to download. Put them in a text file.
    * Ensure all links have the "DOWNLOAD PRODUCT" button at the bottom, indicating a download is avaialble.
2. Use your favourite text editor (like Sublime Text) to select the bold part of the URL, as indicated here. Make a Python list of just this part using regex magic in your text editor.
    * https://www.shapeways.com/product/**VQWXYJZKP**/young-white-dragon
    * The final product of this step should look like: `['GWJWLVDCM','6UQJK8H2W','FK39QN893','S4VY6PPS7','DZNQ6M2YV']`
3. Paste the above part into the `filesToDownload` part of the script.
4. Login the Shapeways in your browser.
5. In a browser like Chrome, go Inspect Element > Network. Click the "DOWNLOAD PRODUCT" button on [any random model](https://www.shapeways.com/product/VQWXYJZKP/young-white-dragon).
6. In the Network tab of Inspect Element, right click on the newly-created document request, then click Copy > As cURL (bash).
7. Go to https://curl.trillworks.com/, and paste in the result. Convert to a Python request string.
8. Paste in just the `headers` dictionary to the `headers` variable in the script.
9. Run the script.

If this was all way too complicated, or there's a step you wish you didn't have to do, let me know and I can work to improve this script.
