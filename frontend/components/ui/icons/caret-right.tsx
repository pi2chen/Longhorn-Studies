import React from "react";
import Svg, { Path } from "react-native-svg";

import type { IconProps } from ".";

import { cssInterop } from "nativewind";

// 1. Tell NativeWind to intercept the `className` prop and apply it as a style to the Svg
cssInterop(Svg, {
  className: {
    target: "style",
  },
});

export default function CaretRightIcon({
  color = "#1A2024",
  size = 24,
  ...props
}: IconProps) {
  return (
    <Svg width={size} height={size} viewBox="0 0 24 24" fill="none" {...props}>
      <Path
        d="M17.0306 12.5307L9.53062 20.0307C9.46094 20.1004 9.37821 20.1556 9.28717 20.1933C9.19612 20.2311 9.09854 20.2505 9 20.2505C8.90145 20.2505 8.80387 20.2311 8.71283 20.1933C8.62178 20.1556 8.53905 20.1004 8.46937 20.0307C8.39969 19.961 8.34441 19.8783 8.3067 19.7872C8.26899 19.6962 8.24958 19.5986 8.24958 19.5001C8.24958 19.4015 8.26899 19.3039 8.3067 19.2129C8.34441 19.1218 8.39969 19.0391 8.46937 18.9694L15.4397 12.0001L8.46937 5.03068C8.32864 4.88995 8.24958 4.69907 8.24958 4.50005C8.24958 4.30103 8.32864 4.11016 8.46937 3.96943C8.6101 3.8287 8.80097 3.74963 9 3.74963C9.19902 3.74963 9.38989 3.8287 9.53062 3.96943L17.0306 11.4694C17.1004 11.5391 17.1557 11.6218 17.1934 11.7128C17.2312 11.8039 17.2506 11.9015 17.2506 12.0001C17.2506 12.0986 17.2312 12.1962 17.1934 12.2873C17.1557 12.3783 17.1004 12.461 17.0306 12.5307Z"
        fill="currentColor"
      />
    </Svg>
  );
}