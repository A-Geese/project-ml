export default function AvatarBig({image, alt, transition }) {
    return (
        <img
          src={image}
          alt={alt}
          className={`w-64 h-64 transition-transform duration-400 ${
            transition ? "translate-x-full opacity-0" : "translate-x-0 opacity-100"
          }`}
        />
    );
  }