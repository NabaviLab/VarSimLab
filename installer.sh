#downloading art_illumina
wget https://www.niehs.nih.gov/research/resources/assets/docs/artbinmountrainier2016.06.05linux64.tgz
tar -xvzf artbinmountrainier2016.06.05linux64.tgz 
cp art_bin_MountRainier/art_illumina .
rm artbinmountrainier2016.06.05linux64.tgz
rm -r art_bin_MountRainier/  

#downloading BEDtools
wget https://github.com/arq5x/bedtools2/releases/download/v2.25.0/bedtools-2.25.0.tar.gz
tar -xvzf bedtools-2.25.0.tar.gz
rm bedtools-2.25.0.tar.gz 
cd bedtools2 
make 
cd ..

#downloading SInC
git clone https://github.com/binaypanda/SiNC.git
#compiling SInC
mv SiNC SInC
cd SInC
unzip SInC_simulator.zip
