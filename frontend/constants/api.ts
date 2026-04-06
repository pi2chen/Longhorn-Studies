import { NativeModules, Platform } from "react-native";

const LOCAL_API_BASE = "http://localhost:8000/api";

const normalizeBaseUrl = (url: string) => url.replace(/\/$/, "");

const getMetroHost = () => {
  const scriptURL = NativeModules.SourceCode?.scriptURL as string | undefined;
  if (!scriptURL) {
    return null;
  }

  const match = scriptURL.match(/\/\/([^/:]+)(?::\d+)?/);
  return match?.[1] ?? null;
};

export const API_BASE = (() => {
  const envBase = process.env.EXPO_PUBLIC_API_BASE_URL?.trim();
  if (envBase) {
    return normalizeBaseUrl(envBase);
  }

  if (Platform.OS === "web") {
    return LOCAL_API_BASE;
  }

  const metroHost = getMetroHost();
  if (metroHost) {
    return `http://${metroHost}:8000/api`;
  }

  return LOCAL_API_BASE;
})();
