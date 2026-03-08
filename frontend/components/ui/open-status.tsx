import { View, Text } from "react-native";
import { ClockIcon } from "./icons";

type OpenStatusType = {
  openStatus: "open" | "closing" | "closed";
  hours?: string[];
};

export default function OpenStatus({ openStatus, hours }: OpenStatusType) {
  const color = `text-status-${openStatus}`;
  return (
    <View className="flex flex-row items-center gap-1">
      <Text className="text-status-open text-status-closing text-status-closed hidden">{/** ENSURES COLORS LOAD PROPERLY */}</Text>
      <ClockIcon
        size={16}
        className={`${color}`}
      />
      <Text
        className={`${color} text-status`}
      >
        {openStatus === "open" && "Open"}
        {openStatus === "closing" && "Closing"}
        {openStatus === "closed" && "Closed"}
      </Text>
      {hours && openStatus !== "closed" && <Text className="text-status text-gray-text">until {hours[1]}</Text>}
      {hours && openStatus === "closed" && <Text className="text-status text-gray-text">until {hours[0]}</Text>}
    </View>
  );
}
