import { View, Text } from "react-native";

type TagProps = {
  tag: string;
};

export function Tag({ tag }: TagProps) {
  return (
    <View className="self-start border border-burnt-orange rounded-full py-1 px-2">
      <Text className="text-burnt-orange text-tag w-fit">{tag}</Text>
    </View>
  );
}
