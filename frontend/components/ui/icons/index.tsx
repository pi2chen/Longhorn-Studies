import { SvgProps } from "react-native-svg";

import ClockIcon from "./clock";
import BookmarkIcon from "./bookmark";
import CaretRightIcon from "./caret-right";
import WalkingIcon from "./walking";
export interface IconProps extends SvgProps {
  color?: string;
  size?: number;
}

export { ClockIcon, BookmarkIcon, CaretRightIcon, WalkingIcon };
