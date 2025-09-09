# S1E2 - ¡El Enigma Cósmico de Kepler-452b! 🌌

[View Challenge](https://makers-challenge.altscore.ai/s1e2)

## Solution Overview
This script solves the cosmic enigma by calculating the average resonance of stars in the Lyra nebula. The challenge requires navigating through paginated star data and processing each star's resonance value.

### Key Features
- Implements a generator to efficiently handle paginated API responses
- Processes star data in batches of 3 stars per page
- Calculates the average resonance across all stars
- Handles API communication and error cases gracefully

## Usage
Run the following command:
```bash
python summit_solution.py
```

### Expected Output
- List of stars with their resonance values and coordinates
- Calculated average resonance
- Success/failure status of the solution submission

## Implementation Notes
- Uses a generator pattern to efficiently handle paginated API responses
- The API returns 3 stars per page, sorted by resonance in descending order
- The solution processes all pages until an empty response is received
- API key is loaded from environment variables (see main README for setup)

### Code Snippet: Star Data Generator
```python
def start_generator(key: str) -> Iterator[dict[str, Any]]:
    headers = {
        'API-KEY': key,
        'accept': 'application/json',
    }
    page = 0
    stars = [1]  # Initialize with non-empty list to start the loop

    while len(stars) > 0:
        page += 1
        params = {
            "page": page,
            "sort-by": "resonance",
            "sort-direction": "desc",
        }
        response = requests.get(
            f"{BASE_URL}/{S1_E2_API_PATH}",
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        stars = response.json()
        yield from stars  # Yield each star in the current page
```

### Note on Headers
While the challenge mentions that headers might contain useful information ("susurros ocultos en los encabezados"), this solution opts for a more robust approach by processing all available pages until an empty response is received, rather than relying on the `x-total-count` header.

## Example Output

These are the sample output after running the script:

```bash
(.venv) fprin@francisco-prin:~/personal/altscore/altscore-solutions/s1_e1_la_sonda_silenciosa$ python summit_solution.py
key:  905cf7df9ad849138f4c26432ebb08b3
[{"id":"f7aed612-be81-434b-9d67-a88f459faedc","resonance":735,"position":{"x":0.009669699608339966,"y":0.07524386007376704,"z":0.883106393300143}},{"id":"478dbd97-50b5-48a6-b08b-9fe34e3f2492","resonance":728,"position":{"x":0.7412309083479308,"y":0.5516804211263913,"z":0.42768691898067934}},{"id":"62e53ca9-c806-4fa2-91a8-330920828c88","resonance":721,"position":{"x":0.7711192230196271,"y":0.6371133773013796,"z":0.2619552624343482}}]
[{"id":"3696ae6c-bd48-4db9-bd87-64daa95ec37f","resonance":714,"position":{"x":0.42357577256372636,"y":0.27668022397225167,"z":0.0035456890877823}},{"id":"3276c056-fd20-4b1b-9d12-94740eda1e67","resonance":707,"position":{"x":0.9053364910793232,"y":0.8461037132948555,"z":0.09229846771273342}},{"id":"f1dfb7c7-3cb5-4bb1-80e2-6e625c93b0d2","resonance":700,"position":{"x":0.6342379588850797,"y":0.2639839016304094,"z":0.48853185214937656}}]
[{"id":"784adfb4-c55c-4f65-a8dc-48627a2ca5ec","resonance":693,"position":{"x":0.6048298270302239,"y":0.7176121871387979,"z":0.20359731232745293}},{"id":"3c5dade5-8f87-4fb7-89d7-e686033ee5b1","resonance":686,"position":{"x":0.10703597770941764,"y":0.5532236408848159,"z":0.2723482123148163}},{"id":"30cd0a61-7efb-4f5b-bd5c-8d2d9d428332","resonance":679,"position":{"x":0.9389300039271039,"y":0.13429111439336772,"z":0.11542867041910221}}]
[{"id":"0d71b14b-c80b-4456-b0ae-31db2fcb4093","resonance":672,"position":{"x":0.8171041351154616,"y":0.2993787521999779,"z":0.6633887149660773}},{"id":"2c5868f5-2527-4df7-bc9c-31e5b40481cb","resonance":665,"position":{"x":0.9872330636315043,"y":0.6539763177107326,"z":0.007823107152157949}},{"id":"6f604c70-2e44-4728-b69f-f03a4d5e9bb4","resonance":658,"position":{"x":0.833744954639807,"y":0.703539925087371,"z":0.6116777657259501}}]
[{"id":"23436157-8e6e-4ce1-a455-652532165e0e","resonance":651,"position":{"x":0.8792702424845428,"y":0.36952708873888396,"z":0.15774683235723197}},{"id":"1a40ee53-bd40-4ab0-9e51-b72f5a3020d5","resonance":644,"position":{"x":0.26520041475040135,"y":0.9332593779937091,"z":0.8808641736864395}},{"id":"9b8afbe5-499a-4180-b82c-1303b0360cef","resonance":637,"position":{"x":0.9960964478550944,"y":0.073260721099633,"z":0.2131543122670404}}]
[{"id":"4471a40d-d981-4c9e-8301-6efa1b9e152b","resonance":630,"position":{"x":0.07254311449315731,"y":0.4582855226185861,"z":0.9984544408544423}},{"id":"be8c3992-87c7-4327-aa2b-1179bcb049be","resonance":623,"position":{"x":0.2999970797987622,"y":0.31617719627185403,"z":0.7518644924144021}},{"id":"f103ec27-526a-4ed5-9f86-3919a66d9c03","resonance":616,"position":{"x":0.23868595261584602,"y":0.3957858467912545,"z":0.6716902229599713}}]
[{"id":"a706ba6e-d003-4e9d-883a-a53a398310b3","resonance":609,"position":{"x":0.9347062577364272,"y":0.20425919942353643,"z":0.7161918007894148}},{"id":"7855c353-32bb-4ada-828f-7d8807421d89","resonance":602,"position":{"x":0.4192249153358725,"y":0.5836722892912247,"z":0.5227827155319589}},{"id":"9a310484-00af-4e7b-b5d9-c87d67f92556","resonance":595,"position":{"x":0.24621534778862486,"y":0.5945191535334412,"z":0.6193815103321031}}]
[{"id":"eb068359-5216-412a-a1f4-d668693b4adf","resonance":588,"position":{"x":0.2352038950009312,"y":0.11988661394712419,"z":0.8902873141294375}},{"id":"17d6b924-fe81-4bdf-9e7c-f95bc105bb77","resonance":581,"position":{"x":0.1858249609807232,"y":0.5950351064500277,"z":0.6752125536040902}},{"id":"c4be24f5-39a0-4496-b20d-904227aa5cbb","resonance":574,"position":{"x":0.15743272793948326,"y":0.9607789032744504,"z":0.08011146524058688}}]
[{"id":"3bed4b8d-cc11-424f-92f9-2de9f6dbf0de","resonance":567,"position":{"x":0.5841775944589712,"y":0.5028503829195136,"z":0.8527198920482854}},{"id":"0be58ca2-129d-4e2d-b2a2-88c8f244b308","resonance":560,"position":{"x":0.5421952013742742,"y":0.7479755603790641,"z":0.05716527290748308}},{"id":"13803957-f308-4bd9-820a-e97c3a6bedf4","resonance":553,"position":{"x":0.2967078254945642,"y":0.9687093649691588,"z":0.5791802908162562}}]
[{"id":"fdce2d4c-d1de-44f4-97cd-7926b978a049","resonance":546,"position":{"x":0.5557683234056182,"y":0.718408275296326,"z":0.15479682527406413}},{"id":"43cbf247-1a69-4cad-b93a-2f504cd6283a","resonance":539,"position":{"x":0.4230074859901629,"y":0.9573176408596732,"z":0.9954226894927138}},{"id":"3c356de1-d388-483c-8210-b19cb37ef895","resonance":532,"position":{"x":0.26520305817215195,"y":0.7840706019485694,"z":0.4550083673391433}}]
[{"id":"e5ee184e-ee3c-4899-874e-d3ecc9704ebe","resonance":525,"position":{"x":0.058635399972178925,"y":0.3789731189769161,"z":0.9853088437797259}},{"id":"e5f73b01-2ac6-4d42-93e2-e98dd0974e5e","resonance":518,"position":{"x":0.48564112545071847,"y":0.21374729919918167,"z":0.4010402925494526}},{"id":"85b94db1-a526-48d0-a501-badd28503230","resonance":511,"position":{"x":0.9263669830081276,"y":0.8486957344143055,"z":0.16631111060391401}}]
[{"id":"2a2d4cf3-6fa3-453c-8adf-f5da2dbd68ac","resonance":504,"position":{"x":0.9992824684127266,"y":0.8360275850799519,"z":0.9689962572847513}},{"id":"baff098c-c1a5-4100-93da-98096b957a08","resonance":497,"position":{"x":0.8613491047618306,"y":0.5503253124498481,"z":0.05058832952488124}},{"id":"d7c15972-6194-4816-840a-7d4b080b2abd","resonance":490,"position":{"x":0.2498064478821005,"y":0.9232655992760128,"z":0.44313074505345695}}]
[{"id":"e14d8917-953f-48f5-8115-1561cea7d684","resonance":483,"position":{"x":0.4486135478331319,"y":0.4218816398344042,"z":0.27854514466694047}},{"id":"af86ceeb-9cf8-4579-88e5-01762cfd3137","resonance":476,"position":{"x":0.8616725363527911,"y":0.24865633392028563,"z":0.1902089084408115}},{"id":"44b6360d-09a2-426d-8b88-d855320a47e3","resonance":469,"position":{"x":0.09841787115195888,"y":0.4026212821022688,"z":0.33930260539496315}}]
[{"id":"ec2e7a0e-837a-4538-9701-96be2365fda3","resonance":462,"position":{"x":0.7290758494598506,"y":0.6733645472933015,"z":0.9841652113659661}},{"id":"0c111f3b-66ab-473f-81f4-ec801b2e3925","resonance":455,"position":{"x":0.4310511824063775,"y":0.4235786230199208,"z":0.467024668036675}},{"id":"bf0a8223-7239-4cc7-a14b-79314675dc3f","resonance":448,"position":{"x":0.8074969977666434,"y":0.1904099143618777,"z":0.09693081422882333}}]
[{"id":"3126a629-6161-41e0-ad2c-c015f9a8273d","resonance":441,"position":{"x":0.5710430933252845,"y":0.47267102631179414,"z":0.7846194242907534}},{"id":"602c7e4b-9f57-4416-899d-db13fc9ba85e","resonance":434,"position":{"x":0.2142368073704386,"y":0.132311848725025,"z":0.935514240580671}},{"id":"17d7ff6b-c3b7-4186-9f1e-06e5a37633a7","resonance":427,"position":{"x":0.07085734988865344,"y":0.23800463436899522,"z":0.6689777782962806}}]
[{"id":"8d24cc3b-88ce-4c50-b17c-77aa1b7a4dc6","resonance":420,"position":{"x":0.22894178381115438,"y":0.905420013006128,"z":0.8596354002537465}},{"id":"bc62ad02-d932-4c2f-8f2c-710f01fe1c94","resonance":413,"position":{"x":0.22021738445155947,"y":0.07099308600903254,"z":0.6311029572700989}},{"id":"5552e84b-d783-4a57-b9f9-b24321f34d62","resonance":406,"position":{"x":0.33808556214745533,"y":0.5883087184572333,"z":0.230114732596577}}]
[{"id":"fd81715a-992a-4b59-8310-a5f02ed0c167","resonance":399,"position":{"x":0.5175758410355906,"y":0.12100419586826572,"z":0.22469733703155736}},{"id":"1bbb9b5a-59a0-466f-82ae-232a9d17e829","resonance":392,"position":{"x":0.9951493566608947,"y":0.6498780576394535,"z":0.43810008391450406}},{"id":"5c982fe1-6eed-48d2-8fa1-49d2a870fd59","resonance":385,"position":{"x":0.7299310690899762,"y":0.2011510633896959,"z":0.31171629130089495}}]
[{"id":"314ad8f8-266d-4391-989b-4976e5413d33","resonance":378,"position":{"x":0.4231379402008869,"y":0.21179820544208205,"z":0.5392960887794583}},{"id":"25faeab0-6b8c-46a6-9ae2-c57c18ecf03f","resonance":371,"position":{"x":0.5498035934949439,"y":0.2650566289400591,"z":0.8724330410852574}},{"id":"5525b2b8-66d1-4b1c-9e6d-5e46b071d31e","resonance":364,"position":{"x":0.7658344293069878,"y":0.1283914644997628,"z":0.4752823780987313}}]
[{"id":"88d5e925-aa86-4c68-b89f-2c3a0df816ae","resonance":357,"position":{"x":0.4859904633166138,"y":0.06921251846838361,"z":0.7606021652572316}},{"id":"d2549cdf-5f00-40c1-a6a8-061438788833","resonance":350,"position":{"x":0.8780095992040405,"y":0.9469494452979941,"z":0.08565345206787878}},{"id":"bc0ce918-6577-438c-9456-e8c53d03d44c","resonance":343,"position":{"x":0.8316655293611794,"y":0.30751412540266143,"z":0.05792516649418755}}]
[{"id":"38463c82-a4f0-44fe-9500-7331e192d427","resonance":336,"position":{"x":0.019476742385832302,"y":0.9290986162646171,"z":0.8787218778231842}},{"id":"bc33116d-0ebe-42c8-8eea-ec27b0e2b4c6","resonance":329,"position":{"x":0.5303536721951775,"y":0.0005718961279435053,"z":0.3241560570046731}},{"id":"eab97c17-8cf6-4afe-8b0d-78ec7f0a7bab","resonance":322,"position":{"x":0.7625108000751513,"y":0.5393790301196257,"z":0.7786264786305582}}]
[{"id":"3ffc0920-076f-4829-a7bc-77e466fdfcb2","resonance":315,"position":{"x":0.6389494948660052,"y":0.6089702114381723,"z":0.1528392685496348}},{"id":"fd1851a0-ecc1-4952-88a1-b21818515375","resonance":308,"position":{"x":0.9126278393448205,"y":0.8705185698367669,"z":0.2984447914486329}},{"id":"a7c40667-603e-45b7-ada6-c2565ce1c0e7","resonance":301,"position":{"x":0.26338905075109076,"y":0.5005861130502983,"z":0.17865188053013137}}]
[{"id":"743b3e47-efbd-4ea4-be96-2bb8ccf53268","resonance":294,"position":{"x":0.45372370632920644,"y":0.9538159275210801,"z":0.8758529403781941}},{"id":"540ca830-9993-4dcf-bd47-4e42e25e8882","resonance":287,"position":{"x":0.6409617985798081,"y":0.11155217359587644,"z":0.434765250669105}},{"id":"f5824434-71b9-4904-9f2e-2638b60468ec","resonance":280,"position":{"x":0.6817103690265748,"y":0.5369703304087952,"z":0.2668251899525428}}]
[{"id":"af700e86-56ae-4c4e-9dfa-098568ee6304","resonance":273,"position":{"x":0.8607797022344981,"y":0.011481021942819636,"z":0.7207218193601946}},{"id":"07a1efa2-dfa5-464c-bc50-9904a128ab36","resonance":266,"position":{"x":0.9961213802400968,"y":0.529114345099137,"z":0.9710783776136181}},{"id":"dbb28dce-688b-40de-9e47-cac459bb8344","resonance":259,"position":{"x":0.42215996679968404,"y":0.06352770615195713,"z":0.38161928650653676}}]
[{"id":"1ec15a76-fe29-4f43-8962-efeb91e556c7","resonance":252,"position":{"x":0.10964913035065915,"y":0.62744604170309,"z":0.7920793643629641}},{"id":"0be5fad1-8872-45dd-b999-806363a2e066","resonance":245,"position":{"x":0.5095262936764645,"y":0.09090941217379389,"z":0.04711637542473457}},{"id":"d400b094-d853-4091-a15b-a1796c228ec0","resonance":238,"position":{"x":0.39940050514039727,"y":0.21932075915728333,"z":0.9975376064951103}}]
[{"id":"848b9cf8-fdd8-4b58-a741-e9c4a0378187","resonance":231,"position":{"x":0.26274160852293527,"y":0.5845859902235405,"z":0.897822883602477}},{"id":"0c79da18-3183-442c-89a6-61d57cb8fc1c","resonance":224,"position":{"x":0.26488016649805246,"y":0.24662750769398345,"z":0.5613681341631508}},{"id":"76f58d34-3c0d-41b4-af2e-d9d796f2b936","resonance":217,"position":{"x":0.39563190106066426,"y":0.9145475897405435,"z":0.4588518525873988}}]
[{"id":"55aa0237-6d96-40f2-9a25-a46d2f234c35","resonance":210,"position":{"x":0.8763676264726689,"y":0.3146778807984779,"z":0.65543866529488}},{"id":"00d25618-a4a0-4eed-913b-15ec40eb7234","resonance":203,"position":{"x":0.26774087597570273,"y":0.21098284358632646,"z":0.9429097143350544}},{"id":"6934fb1d-0c28-4738-89ea-af2f52621413","resonance":196,"position":{"x":0.22904807196410437,"y":0.03210024390403776,"z":0.3154530480590819}}]
[{"id":"41d48692-da31-4ef1-a4dc-ec7cfe797def","resonance":189,"position":{"x":0.6846142509898746,"y":0.8428519201898096,"z":0.7759999115462448}},{"id":"0f794076-41e3-4118-96b4-55afd5e550bb","resonance":182,"position":{"x":0.9895233506365952,"y":0.6399997598540929,"z":0.5569497437746462}},{"id":"5d18e7b8-b251-4cbb-9568-c6ff26ee64c1","resonance":175,"position":{"x":0.7291267979503492,"y":0.1634024937619284,"z":0.3794554417576478}}]
[{"id":"faa6e806-4e52-491c-a3aa-f47df9087379","resonance":168,"position":{"x":0.6480353852465935,"y":0.6091310056669882,"z":0.171138648198097}},{"id":"ece40b7c-57de-469a-82d6-8f35e1aa21ad","resonance":161,"position":{"x":0.2095070307714877,"y":0.26697782204911336,"z":0.936654587712494}},{"id":"19b4a88f-1cbd-48b2-b656-b26cf0e69e5d","resonance":154,"position":{"x":0.6356844442644002,"y":0.36483217897008424,"z":0.37018096711688264}}]
[{"id":"b8dc17e5-348d-47bf-a96c-62e0dff78991","resonance":147,"position":{"x":0.23279088636103018,"y":0.10100142940972912,"z":0.2779736031100921}},{"id":"c2318e1d-26e1-47d6-83bd-bd950381aee2","resonance":140,"position":{"x":0.22789827565154686,"y":0.28938796360210717,"z":0.0797919769236275}},{"id":"fe05a4b2-9bad-4ea8-95ff-e9c9b258ec2c","resonance":133,"position":{"x":0.577352145256762,"y":0.7045718362149235,"z":0.045824383655662215}}]
[{"id":"6d3722e3-5e15-4343-8066-888d3508e22d","resonance":126,"position":{"x":0.8294046642529949,"y":0.6185197523642461,"z":0.8617069003107772}},{"id":"d201ec90-6dc5-4653-ab80-c5a28dd3ec64","resonance":119,"position":{"x":0.9731157639793706,"y":0.3785343772083535,"z":0.552040631273227}},{"id":"62ee4831-1805-4b49-9bc4-8e9bbc28abc3","resonance":112,"position":{"x":0.8071282732743802,"y":0.7297317866938179,"z":0.5362280914547007}}]
[{"id":"61b85414-aea0-418c-94ff-718945bfbd08","resonance":105,"position":{"x":0.09671637683346401,"y":0.8474943663474598,"z":0.6037260313668911}},{"id":"20a5aae3-ff6f-48e1-bdd5-9fe5d9e14557","resonance":98,"position":{"x":0.9572130722067812,"y":0.33659454511262676,"z":0.09274584338014791}},{"id":"5921e530-724d-45d6-97ee-c110fa15fe11","resonance":91,"position":{"x":0.6981393949882269,"y":0.3402505165179919,"z":0.15547949981178155}}]
[{"id":"8294e604-3c43-488b-99e7-3a849b7c007b","resonance":84,"position":{"x":0.8094304566778266,"y":0.006498759678061017,"z":0.8058192518328079}},{"id":"c590ec32-924b-456b-b65d-496b602cdbc9","resonance":77,"position":{"x":0.5449414806032167,"y":0.2204406220406967,"z":0.5892656838759087}},{"id":"c24d6e97-e1f1-40e3-ac3a-9fa4c63f818e","resonance":70,"position":{"x":0.026535969683863625,"y":0.1988376506866485,"z":0.6498844377795232}}]
[{"id":"93e2bfc9-9ea4-41c4-9391-dbe1e7f59dbb","resonance":63,"position":{"x":0.029797219438070344,"y":0.21863797480360336,"z":0.5053552881033624}},{"id":"b74118c1-7042-4fcc-a412-c0cd94d5b88a","resonance":56,"position":{"x":0.8921795677048454,"y":0.08693883262941615,"z":0.4219218196852704}},{"id":"a20ccf98-3c83-44f7-a614-523308baeb4b","resonance":49,"position":{"x":0.22321073814882275,"y":0.7364712141640124,"z":0.6766994874229113}}]
[{"id":"4eb2d241-8ca4-4215-a0ae-b98dfbb542cc","resonance":42,"position":{"x":0.6394267984578837,"y":0.025010755222666936,"z":0.27502931836911926}}]
[]
{'average_resonance': 388}
{"result":"correct"}
{'result': 'correct'}
```
