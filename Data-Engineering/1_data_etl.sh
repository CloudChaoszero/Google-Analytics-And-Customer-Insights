mkdir -p ../Resources/Data/ZipFiles
mkdir -p ../Resources/Data/RawData


kaggle competitions download -c ga-customer-revenue-prediction -p ../Resources/Data/ZipFiles

# tar xvf ../Resources/Data/ZipFiles/\* -d ../Resources/Data/RawData
# tar -xvf ../Resources/Data/ZipFiles/\* -d ../Resources/Data/RawData
unzip ../Resources/Data/ZipFiles/\* -d ../Resources/Data/RawData


python 2_transformation_load.py