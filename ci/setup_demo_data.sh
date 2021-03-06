mkdir -p data/simulations/test-sim{1,2}/fake_date_sample_{0,1}/reads/
mkdir -p data/simulations/test-sim3/fake_date3_sample_{0,1}/reads/
echo '' > data/simulations/test-sim1/fake_date_sample_0/reads/anonymous_reads.fq.gz
echo '' > data/simulations/test-sim2/fake_date_sample_0/reads/anonymous_reads.fq.gz
echo '' > data/simulations/test-sim1/fake_date_sample_1/reads/anonymous_reads.fq
echo '' > data/simulations/test-sim3/fake_date3_sample_0/reads/anonymous_reads.fq
echo '' > data/simulations/test-sim1/taxonomic_profile_0.txt
echo '' > data/simulations/test-sim2/taxonomic_profile_0.txt
echo '' > data/simulations/test-sim1/taxonomic_profile_1.txt
echo '' > data/simulations/test-sim3/taxonomic_profile_0.txt
mkdir -p data/profiles/test-sim{1,2,3}/blah/
for eachfile in data/profiles/test-sim{1,2}/blah/fake_date_sample_{0,1}.family.profile.txt; do
  echo '' > $eachfile
done
for eachfile in data/profiles/test-sim{1,2}/blah/fake_date_sample_{0,1}.genus.profile.txt; do
  echo '' > $eachfile
done
mkdir -p data/profiles/test-sim{1,2,3}/mohawk_{0,1,2,3}/
for eachfile in data/profiles/test-sim{1,2,3}/mohawk_{0,1,2,3}/fake_date_sample_{0,1}.family.profile.txt; do
  echo '' > $eachfile
done
for eachfile in data/profiles/test-sim3/mohawk_{0,1,2,3}/fake_date3_sample_0.family.profile.txt; do
  echo '' > $eachfile
done
