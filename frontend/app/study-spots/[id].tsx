import { Ionicons } from "@expo/vector-icons";
import { Image } from "expo-image";
import { Stack, useLocalSearchParams, useRouter } from "expo-router";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import OpenStatus from "@/components/ui/open-status";
import { BookmarkIcon } from "@/components/ui/icons";
import { Tag } from "@/components/ui/tags";
import { API_BASE } from "@/constants/api";

type OpenState = "open" | "closing" | "closed";
type AccessWindow = [string, string];

type StudySpot = {
  id: number;
  abbreviation: string;
  study_spot_name: string;
  building_name: string | null;
  address: string;
  floor: number | null;
  tags: string[];
  pictures: string[];
  access_hours: AccessWindow[];
  capacity: number;
  description: string;
  rating: number;
  review_count: number;
};

// eslint-disable-next-line @typescript-eslint/no-require-imports
const HERO_FALLBACK_IMAGE = require("@/assets/images/study-spot-hero-placeholder.jpg");
// eslint-disable-next-line @typescript-eslint/no-require-imports
const MAP_PREVIEW_IMAGE = require("@/assets/images/map-preview-placeholder.png");
const PLACEHOLDER_ACCESS_HOURS: AccessWindow[] = [
  ["08:00", "17:00"],
  ["08:00", "17:00"],
  ["08:00", "17:00"],
  ["08:00", "17:00"],
  ["08:00", "17:00"],
  ["00:00", "00:00"],
  ["00:00", "00:00"],
];

const weekDayIndex = (date = new Date()) => (date.getDay() + 6) % 7;

const toMinutes = (value: string) => {
  const [hour, minute] = value.split(":").map(Number);
  if (Number.isNaN(hour) || Number.isNaN(minute)) {
    return 0;
  }
  return hour * 60 + minute;
};

const toDisplayTime = (value: string) => {
  const [hour, minute] = value.split(":").map(Number);
  if (Number.isNaN(hour) || Number.isNaN(minute)) {
    return value;
  }

  const suffix = hour >= 12 ? "PM" : "AM";
  const twelveHour = hour % 12 === 0 ? 12 : hour % 12;
  return `${twelveHour}:${minute.toString().padStart(2, "0")} ${suffix}`;
};

const isClosedWindow = ([open, close]: AccessWindow) => open === "00:00" && close === "00:00";

const getTodayWindow = (hours: AccessWindow[]) => hours[weekDayIndex()] ?? ["00:00", "00:00"];

const getOpenState = (hours: AccessWindow[], now = new Date()): OpenState => {
  const [open, close] = getTodayWindow(hours);
  if (isClosedWindow([open, close])) {
    return "closed";
  }

  const openMinutes = toMinutes(open);
  const closeMinutes = toMinutes(close);
  const currentMinutes = now.getHours() * 60 + now.getMinutes();

  // Handle overnight windows where close time is after midnight (e.g. 20:00–02:00).
  const isOvernight = closeMinutes <= openMinutes;
  const adjustedCloseMinutes = isOvernight ? closeMinutes + 24 * 60 : closeMinutes;
  const adjustedCurrentMinutes =
    isOvernight && currentMinutes < openMinutes ? currentMinutes + 24 * 60 : currentMinutes;

  const isOpenNow =
    adjustedCurrentMinutes >= openMinutes && adjustedCurrentMinutes < adjustedCloseMinutes;
  if (!isOpenNow) {
    return "closed";
  }

  if (adjustedCloseMinutes - adjustedCurrentMinutes <= 60) {
    return "closing";
  }

  return "open";
};

const getWeekdaySummary = (hours: AccessWindow[]) => {
  const weekdays = hours.slice(0, 5);
  if (weekdays.length === 5) {
    const [baseOpen, baseClose] = weekdays[0];
    const allSame = weekdays.every(([open, close]) => open === baseOpen && close === baseClose);

    if (allSame) {
      if (isClosedWindow([baseOpen, baseClose])) {
        return "Mon - Fri: Closed";
      }
      return `Mon - Fri: ${toDisplayTime(baseOpen)} - ${toDisplayTime(baseClose)}`;
    }
  }

  const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const dayName = dayNames[weekDayIndex()];
  const [open, close] = getTodayWindow(hours);
  if (isClosedWindow([open, close])) {
    return `${dayName}: Closed`;
  }
  return `${dayName}: ${toDisplayTime(open)} - ${toDisplayTime(close)}`;
};

const toAddressLine = (spot: StudySpot) =>
  `${spot.address}${spot.floor !== null ? ` - Level ${spot.floor}` : ""}`;

const getPlaceholderSpot = (id: number): StudySpot => ({
  id: Number.isFinite(id) ? id : 1,
  abbreviation: "SZB",
  study_spot_name: "Student Lounge",
  building_name: "George I. Sanchez Building",
  address: "1912 Speedway",
  floor: 1,
  tags: ["Lounge", "Low Noise", "Outlets"],
  pictures: [HERO_FALLBACK_IMAGE],
  access_hours: PLACEHOLDER_ACCESS_HOURS,
  capacity: 30,
  description:
    "A student lounge located near the East entrance of SZB with large windows, cozy seating, plenty of outlets, and a printer.",
  rating: 4.2,
  review_count: 13,
});

export default function StudySpotDetailsScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { id } = useLocalSearchParams<{ id: string }>();

  const [spot, setSpot] = useState<StudySpot | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isPlaceholderData, setIsPlaceholderData] = useState(false);

  const numericId = useMemo(() => Number(id), [id]);

  const loadStudySpot = useCallback(async () => {
    if (!Number.isFinite(numericId)) {
      setSpot(getPlaceholderSpot(1));
      setIsPlaceholderData(true);
      setError(null);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);
    setIsPlaceholderData(false);

    try {
      const response = await fetch(`${API_BASE}/study_spots/${numericId}`);
      if (!response.ok) {
        throw new Error(`Failed with status ${response.status}`);
      }

      const data = (await response.json()) as StudySpot;
      setSpot(data);
      setIsPlaceholderData(false);
    } catch {
      setSpot(getPlaceholderSpot(numericId));
      setIsPlaceholderData(true);
      setError(null);
    } finally {
      setIsLoading(false);
    }
  }, [numericId]);

  useEffect(() => {
    loadStudySpot();
  }, [loadStudySpot]);

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-white">
        <Stack.Screen options={{ headerShown: false }} />
        <ActivityIndicator size="large" color="#BF5700" />
        <Text className="mt-3 text-main-text font-roboto">Loading details...</Text>
      </View>
    );
  }

  if (error || !spot) {
    return (
      <View className="flex-1 items-center justify-center px-6 bg-white">
        <Stack.Screen options={{ headerShown: false }} />
        <Text className="text-main-text text-center font-roboto">
          {error ?? "Study spot not found."}
        </Text>
        <View className="mt-4 flex-row gap-2">
          <Pressable
            className="border border-burnt-orange rounded-full px-4 py-2"
            onPress={loadStudySpot}
          >
            <Text className="text-burnt-orange font-roboto">Retry</Text>
          </Pressable>
          <Pressable
            className="border border-card-border rounded-full px-4 py-2"
            onPress={() => router.back()}
          >
            <Text className="text-main-text font-roboto">Back</Text>
          </Pressable>
        </View>
      </View>
    );
  }

  const openState = getOpenState(spot.access_hours);
  const weeklyHoursSummary = getWeekdaySummary(spot.access_hours);
  const heroImage = spot.pictures?.[0] ?? HERO_FALLBACK_IMAGE;

  const fullStars = Math.floor(spot.rating);
  const hasHalfStar = spot.rating - fullStars >= 0.1;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

  return (
    <View className="flex-1 bg-white">
      <Stack.Screen options={{ headerShown: false }} />

      <ScrollView contentContainerStyle={{ paddingBottom: 90 + insets.bottom }}>
        {/* Hero image */}
        <View className="relative">
          <Image source={heroImage} contentFit="cover" style={{ width: "100%", height: 281 }} />

          <View
            className="absolute left-2 right-2 flex-row items-center justify-between"
            style={{ top: insets.top + 8 }}
          >
            <TouchableOpacity
              className="size-9 rounded-full bg-white items-center justify-center"
              onPress={() => router.back()}
              activeOpacity={0.8}
            >
              <Ionicons name="arrow-back" size={20} color="#333F48" />
            </TouchableOpacity>

            <TouchableOpacity
              className="size-9 rounded-full bg-white items-center justify-center"
              activeOpacity={0.8}
            >
              <BookmarkIcon size={20} color="#333F48" />
            </TouchableOpacity>
          </View>

          <View className="absolute bottom-3 left-0 right-0 flex-row items-center justify-center gap-2">
            <View className="size-1.5 rounded-full bg-white/70" />
            <View className="size-1.5 rounded-full bg-white/70" />
          </View>
        </View>

        <View className="px-3 pt-4">
          {isPlaceholderData && (
            <View className="mb-2 self-start rounded-full border border-burnt-orange/60 bg-active-filter px-3 py-1">
              <Text className="text-tag text-burnt-orange font-roboto">Placeholder Data</Text>
            </View>
          )}

          {/* Name */}
          <Text className="text-details-header text-main-text font-roboto font-medium">
            <Text className="text-burnt-orange font-bold">{spot.abbreviation}</Text>{" "}
            {spot.study_spot_name}
          </Text>

          {/* Address */}
          <View className="mt-1 flex-row items-center gap-1 px-1">
            <Ionicons name="location-outline" size={15} color="#94A3B8" />
            <Text className="text-spot-name text-gray-text font-roboto font-medium">
              {toAddressLine(spot)}
            </Text>
          </View>

          {/* Open status + Hours row */}
          <View className="mt-2 flex-row items-center gap-2">
            <OpenStatus openStatus={openState} />
            <Text className="text-base-16 text-main-text font-roboto">{weeklyHoursSummary}</Text>
            <Ionicons name="chevron-down" size={18} color="#333F48" />
          </View>

          {/* Rating */}
          <View className="mt-2 flex-row items-center gap-2">
            <Text className="text-base-16 text-main-text font-roboto font-medium">
              {spot.rating.toFixed(1)}
            </Text>
            <View className="flex-row items-center gap-1">
              {Array.from({ length: fullStars }).map((_, i) => (
                <Ionicons key={`full-${i}`} name="star" size={20} color="#BF5700" />
              ))}
              {hasHalfStar && <Ionicons name="star-half" size={20} color="#BF5700" />}
              {Array.from({ length: emptyStars }).map((_, i) => (
                <Ionicons key={`empty-${i}`} name="star-outline" size={20} color="#BF5700" />
              ))}
            </View>
            <Text className="text-base-16 text-gray-text font-roboto">
              ({spot.review_count})
            </Text>
          </View>

          {/* Divider */}
          <View className="mt-4 h-px bg-card-border/80" />

          {/* Full Building Name */}
          <View className="mt-4">
            <View className="flex-row items-center gap-1">
              <Ionicons name="business-outline" size={16} color="#94A3B8" />
              <Text className="text-spot-name text-gray-text font-roboto font-medium">
                Full Building Name
              </Text>
            </View>
            <Text className="mt-1 text-base-16 text-main-text font-roboto">
              {spot.building_name ?? "N/A"}
            </Text>
          </View>

          {/* Estimated Capacity */}
          <View className="mt-4">
            <View className="flex-row items-center gap-1">
              <Ionicons name="people-outline" size={18} color="#94A3B8" />
              <Text className="text-spot-name text-gray-text font-roboto font-medium">
                Estimated Capacity
              </Text>
            </View>
            <Text className="mt-1 text-base-16 text-main-text font-roboto">{spot.capacity}</Text>
          </View>

          {/* Tags */}
          <View className="mt-4 flex-row flex-wrap gap-2">
            {spot.tags.slice(0, 4).map((tag, index) => (
              <Tag key={`${tag}-${index}`} tag={tag} />
            ))}
          </View>

          {/* Map preview */}
          <View className="mt-4 overflow-hidden rounded-xl border border-card-border relative">
            <Image source={MAP_PREVIEW_IMAGE} contentFit="cover" style={{ width: "100%", height: 283 }} />
            <TouchableOpacity
              className="absolute right-3 top-3 size-9 rounded-full bg-white items-center justify-center"
              activeOpacity={0.8}
            >
              <Ionicons name="expand-outline" size={18} color="#11181C" />
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>

      <View
        className="absolute bottom-0 left-0 right-0 border-t border-[#D6D2C4] bg-white"
        style={{ paddingBottom: Math.max(insets.bottom, 10) }}
      >
        <View className="h-[62px] flex-row items-center justify-center gap-20">
          <Ionicons name="home" size={28} color="#BF5700" />
          <Ionicons name="location-sharp" size={24} color="#BAC1CC" />
          <Ionicons name="person" size={26} color="#BAC1CC" />
        </View>
      </View>
    </View>
  );
}
