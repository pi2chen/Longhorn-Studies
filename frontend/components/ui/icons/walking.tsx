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

export default function WalkingIcon({
  color = "#94A3B8",
  size = 14, 
  ...props
}: IconProps) {
  return (
    <Svg width={size} height={size} viewBox="0 0 14 14" fill="none" {...props}>
      <Path
        d="M7.875 3.20833C8.51667 3.20833 9.04167 2.68333 9.04167 2.04167C9.04167 1.4 8.51667 0.875 7.875 0.875C7.23333 0.875 6.70833 1.4 6.70833 2.04167C6.70833 2.68333 7.23333 3.20833 7.875 3.20833ZM5.71667 5.19167L4.08333 13.4167H5.30833L6.35833 8.75L7.58333 9.91667V13.4167H8.75V9.04167L7.525 7.875L7.875 6.125C8.63333 7 9.8 7.58333 11.0833 7.58333V6.41667C9.975 6.41667 9.04167 5.83333 8.575 5.01667L7.99167 4.08333C7.75833 3.73333 7.40833 3.5 7 3.5C6.825 3.5 6.70833 3.55833 6.53333 3.55833L3.5 4.84167V7.58333H4.66667V5.6L5.71667 5.19167Z"
        fill="currentColor"
      />
    </Svg>
  );
}