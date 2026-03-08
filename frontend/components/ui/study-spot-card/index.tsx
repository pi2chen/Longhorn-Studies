import { Image } from "expo-image";

import { View, Text, TouchableOpacity } from "react-native";

import OpenStatus from "../open-status";
import { Tag } from "../tags";

import { BookmarkIcon, CaretRightIcon, WalkingIcon } from "../icons";

const blurhash =
  "|rF?hV%2WCj[ayj[a|j[az_NaeWBj@ayfRayfQfQM{M|azj[azf6fQfQfQIpWXofj[ayj[j[fQayWCoeoeaya}j[ayfQa{oLj?j[WVj[ayayj[fQoff7azayj[ayj[j[ayofayayayj[fQj[ayayj[ayfjj[j[ayjuayj[";

type StudySpotCardType = {
  locationName: string;
  buildingName: string;
  location: string; // TODO: get proper type
  hours: string[];
  tags: string[];
};
export default function StudySpotCard({
  locationName,
  buildingName,
  hours,
  tags,
}: StudySpotCardType) {
  return (
    <View className="flex flex-row gap-2 border p-2 rounded-lg border-card-border">
      <View className="w-[78px] aspect-square relative bg-blue-500 rounded">
        <Image
          source="https://www.rambleratx.com/wp-content/uploads/2022/06/Texas-Union.jpeg"
          placeholder={{ blurhash }}
          contentFit="cover"
          transition={1000}
          style={{ width: "100%", height: "100%", borderRadius: 4 }}
        />
        <TouchableOpacity
          className="bg-saved-bg rounded-full self-start p-1 absolute top-1 left-1"
          onPress={() => console.log("Bookmark tapped!")}
          hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
        >
          <BookmarkIcon size={16} className="text-white" />
        </TouchableOpacity>
      </View>
      <View className="flex justify-between">
        <View>
          <View className="flex flex-row">
            <Text className="text-spot-name text-burnt-orange font-bold">
              {buildingName}
            </Text>
            <Text className="text-spot-name font-bold"> {locationName}</Text>
          </View>
          <View className="flex flex-row items-center gap-3">
            <View className="flex flex-row gap-1">
              <WalkingIcon size={14} className="text-gray-text" />
              <Text className="text-gray-text text-status">0.1 mi</Text>
            </View>
            <OpenStatus openStatus="open" hours={["5:00am", "5:00pm"]} />
          </View>
        </View>
        <View className="flex flex-row gap-1">
          <Tag tag="Lounge" />
          <Tag tag="Low Noise" />
          <Tag tag="Near Food & Cafe" />
        </View>
      </View>
      <View className="flex justify-center ml-auto">
        <CaretRightIcon size={12} className="text-gray-400" />
      </View>
    </View>
  );
}
