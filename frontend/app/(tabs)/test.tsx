import { Image } from "expo-image";
import { View } from "react-native";

import StudySpotCard from "@/components/ui/study-spot-card";

export default function HomeScreen() {
  return (
    <View className="p-4">
    <Image
        source="https://picsum.photos/seed/696/3000/2000"
        contentFit="cover"
        transition={1000}
        className="w-full h-64 rounded-xl"
        style={{ width: '100%', height: 250 }}
      />
      <View className="h-64" />
      <View className="h-16" />
      <StudySpotCard buildingName="Union" locationName="Ballroom" location="Ballroom" hours={["5:00am", "5:00pm"]} tags={["Hi"]}/>
    </View>
  );
}
