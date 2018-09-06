import lolalyticsStats
import designerDefs

designers = designerDefs.designers
champions = designerDefs.champions
champion_array = []
# do data gathering by champion
for champion_name, champion in champions.iteritems():
	champion["winrate"] = lolalyticsStats.getWinrate(champion_name)
	champion["pickrate"] = lolalyticsStats.getPickrate(champion_name)
	champion["banrate"] = lolalyticsStats.getBanrate(champion_name)
	champion["hate"] = champion["banrate"] / lolalyticsStats.getInfluence(champion_name)

	# add to designers champion arrays
	for designer in champion["designers"]:
		designers[designer]["champions"].append(champion)

	#add to champions array
	champion["name"] = champion_name
	champion_array.append(champion)

designer_array = []
# do data aggregation by designer
for designer_name, designer in designers.iteritems():
	designer["numChampions"] = len(designer["champions"])

	if designer["numChampions"] > 1:
		total_pickrate = 0
		total_banrate = 0
		average_winrate = 0
		for champion in designer["champions"]:
			total_pickrate += champion["pickrate"]
			total_banrate += champion["banrate"]

		for champion in designer["champions"]:
			average_winrate += (champion["winrate"] * (champion["pickrate"] / total_pickrate))

		designer["average_pickrate"] = total_pickrate / designer["numChampions"]
		designer["average_banrate"] = total_banrate / designer["numChampions"]
		designer["average_winrate"] = average_winrate
		designer["power"] = ((100 * designer["average_pickrate"]) /
                            (100 - designer["average_banrate"])) * (designer["average_winrate"] - 50)
		designer["hate"] = designer["average_banrate"] / designer["power"]

		designer["name"] = designer_name
		del designer["champions"]
		designer_array.append(designer)

print("Most Champions Designed")
print("Name|Number of Champions|Champion Power Score|Avg Winrate|Avg Banrate|Avg Pickrate|Champion Hate Score")
print(":--|:-:|:-:|:-:|:-:|:-:|:-:|:-:")
for designer in sorted(designer_array, key=lambda x: x["numChampions"], reverse=True):
	print(designer["name"] + "|" +
		  str(designer["numChampions"]) + "|" +
		  str(round(designer["power"], 1)) + "|" +
		  str(round(designer["average_winrate"], 1)) + "|" +
		  str(round(designer["average_banrate"], 1)) + "|" +
		  str(round(designer["average_pickrate"], 1)) + "|" +
		  str(round(designer["hate"], 1)))

print("\n")
print("Power")
print("Name|Champion Power Score|Number of Champions")
print(":--|:-:|:-:")
for designer in sorted(designer_array, key=lambda x: x["power"], reverse=True):
	print(designer["name"] + "|" +
		  str(round(designer["power"], 1)) + "|" +
		  str(designer["numChampions"]))

print("\n")
print("Average Pickrate")
print("Name|Avg Pickrate|Number of Champions")
print(":--|:-:|:-:")
for designer in sorted(designer_array, key=lambda x: x["average_pickrate"], reverse=True):
	print(designer["name"] + "|" +
		  str(round(designer["average_pickrate"], 1)) + "|" +
		  str(designer["numChampions"]))

print("\n")
print("Average Banrate")
print("Name|Avg Banrate|Number of Champions")
print(":--|:-:|:-:")
for designer in sorted(designer_array, key=lambda x: x["average_banrate"], reverse=True):
	print(designer["name"] + "|" +
		  str(round(designer["average_banrate"], 1)) + "|" +
		  str(designer["numChampions"]))

print("\n")
print("Champion Hate Score")
print("Name|Champion Hate Score|Number of Champions")
print(":--|:-:|:-:")
for designer in sorted(designer_array, key=lambda x: x["hate"], reverse=True):
	print(designer["name"] + "|" +
		  str(round(designer["hate"], 1)) + "|" +
		  str(designer["numChampions"]))