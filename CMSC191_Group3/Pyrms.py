from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt
import re
from numpy import array


class Pyrms:
    all = []
    pyrms_dictionary = {}
    location_dictionary = {}

    def __init__(self, name: str, country: str, location: str, collected_by: str, populations: str, individuals: str,
                 size: int):
        self.__name = name
        self.__location = f"{country}, {location}"
        self.__collected_by = collected_by
        self.__populations = populations
        self.__individuals = individuals
        self.__size = size

        Pyrms.all.append(self)

    @classmethod
    def read_csv(cls, filename):
        csv_df = read_csv(filename)
        return csv_df

    @classmethod
    def extract_samples(cls, cls_df):
        sample_pattern = re.compile(r"^Pyrms\d+[a-z]*-\d+[a-z]*$")
        samples = df.columns.values.tolist()
        sample_names = []
        for i in samples:
            mo = sample_pattern.search(i)
            if mo:
                sample_names.append(mo.group())
        return sample_names

    @classmethod
    def instantiate_sample_objects(cls, data_frame, sample_names):
        for i in range(0, len(sample_names)):
            for j in range(0, len(df.axes[0])):
                Pyrms(
                    name=sample_names[i],
                    country=data_frame.at[j, "country"],
                    location=data_frame.at[j, "location"],
                    collected_by=data_frame.at[j, "collected by"],
                    populations=data_frame.at[j, "populations"],
                    individuals=data_frame.at[j, "individuals"],
                    size=data_frame.at[j, sample_names[i]]
                )

    @classmethod
    def compute_sample_distribution(cls, sample_names):  # method for the overall summary
        for i in sample_names:
            pyrm_sizes = []
            for j in Pyrms.all:
                if j.name == i:
                    pyrm_sizes.append(j.size)

            unique_sizes = list(set(pyrm_sizes))
            unique_sizes_count = []

            for j in unique_sizes:
                size_count = pyrm_sizes.count(j)
                unique_sizes_count.append([str(j), size_count])

            Pyrms.pyrms_dictionary[i] = unique_sizes_count

        return Pyrms.pyrms_dictionary

    @classmethod
    def compute_location_distribution(cls,sample_names):  # method for the location view that contains the stacked bar graph of pyrms
        locations = []
        pyrms_location = {}

        for i in Pyrms.all:
            locations.append(i.location)

        locations = list(set(locations))

        for sample in sample_names:
            location_size = {}
            for loc in locations:
                size_array = []
                for obj in Pyrms.all:
                    if obj.name == sample and obj.location == loc:
                        size_array.append(obj.size)

                unique_size_array = list(set(size_array))
                unique_sizes_count = []

                for size in unique_size_array:
                    size_count = size_array.count(size)
                    unique_sizes_count.append([str(size), size_count])

                location_size[loc] = unique_sizes_count
            pyrms_location[sample] = location_size

        return pyrms_location

    def __repr__(self):
        return f"Pyrms({self.__name}, {self.__location}, {self.__collected_by}, {self.__populations}, {self.__individuals}, {self.__size})"

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def collected_by(self):
        return self.__collected_by

    @property
    def populations(self):
        return self.__populations

    @property
    def individuals(self):
        return self.__individuals

    @property
    def size(self):
        return self.__size


df = Pyrms.read_csv("Dataset-Saleh-et-al.csv")
names = Pyrms.extract_samples(df)
Pyrms.instantiate_sample_objects(df, names)
overall_distribution = Pyrms.compute_sample_distribution(names)
location_distribution = Pyrms.compute_location_distribution(names)

# make a data form out of the dictionaries
overall_distribution_df = []
for i in overall_distribution:
    overall_distribution_df.append(DataFrame(overall_distribution[i], columns=["Length", "Count"]))

location_distribution_df = []
for i in location_distribution:
    for j in location_distribution[i]:
        location_distribution_df.append(DataFrame(location_distribution[i][j], columns=["Length", "Count"]))







