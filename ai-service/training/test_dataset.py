from dataset import EmotionDataset


dataset = EmotionDataset("../data/emotions.csv")


print("Toplam veri:", len(dataset))


item = dataset[0]


print(item)