# Longhorn Studies Frontend

This is a React Native application built with Expo that works on web, iOS, and Android.

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Installation

```bash
npm install
```

## Running the App

### Web
```bash
npm run web
```

### iOS (requires macOS with Xcode)
```bash
npm run ios
```

### Android (requires Android Studio)
```bash
npm run android
```

### Development Server
```bash
npm start
```

This will start the Expo development server. You can then:
- Press `w` to open in web browser
- Press `a` to open in Android emulator
- Press `i` to open in iOS simulator
- Scan the QR code with Expo Go app on your physical device

## Configuration

The app connects to the backend API at `http://localhost:8000/api` by default. To change this:

1. Open `App.js`
2. Modify the `API_BASE_URL` constant at the top of the file

## Features

- View items from the backend database
- Add new items
- Delete items
- Automatic refresh on load
- Cross-platform compatibility (Web, iOS, Android)

## Project Structure

```
frontend/
├── App.js              # Main application component
├── app.json            # Expo configuration
├── babel.config.js     # Babel configuration
├── package.json        # Dependencies and scripts
└── README.md          # This file
```
