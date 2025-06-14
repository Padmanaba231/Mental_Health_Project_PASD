import React from "react";
import {
  Navbar,
  Collapse,
  Typography,
  Button,
  IconButton,
} from "@material-tailwind/react";
import { Link, useLocation } from "react-router-dom";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";

export default function NavbarWithSolidBackground() {
  const [openNav, setOpenNav] = React.useState(false);
  const location = useLocation();

  React.useEffect(() => {
    window.addEventListener("resize", () => {
      if (window.innerWidth >= 960) setOpenNav(false);
    });
  }, []);

  const navItems = [
    { label: "Home", to: "/" },
    { label: "Chatbot", to: "/chatbot" },
    { label: "Profile", to: "/profile" },
  ];

  const navList = (
    <ul className="mb-4 mt-2 flex flex-col gap-2 lg:mb-0 lg:mt-0 lg:flex-row lg:items-center lg:gap-6">
      {navItems.map((item) => (
        <Typography
          key={item.to}
          as="li"
          variant="small"
          color="blue-gray"
          className={`p-1 font-normal ${
            location.pathname === item.to ? "text-teal-600 font-semibold" : ""
          }`}
        >
          <Link to={item.to} className="flex items-center">
            {item.label}
          </Link>
        </Typography>
      ))}
    </ul>
  );

  return (
    <Navbar className="sticky top-0 z-50 h-max max-w-full bg-gray-100 rounded-none px-4 py-2 lg:px-8 lg:py-4">
      <div className="flex items-center justify-between text-blue-gray-900">
        <Typography as={Link} to="/" className="mr-4 cursor-pointer py-1.5 font-bold text-teal-700">
          PASD
        </Typography>
        <div className="hidden lg:block">{navList}</div>
        <Button
          as={Link}
          to="/login"
          variant="gradient"
          size="sm"
          className="hidden lg:inline-block"
        >
          <span>Login</span>
        </Button>
        <IconButton
          variant="text"
          className="lg:hidden"
          onClick={() => setOpenNav(!openNav)}
        >
          {openNav ? (
            <XMarkIcon className="h-6 w-6" strokeWidth={2} />
          ) : (
            <Bars3Icon className="h-6 w-6" strokeWidth={2} />
          )}
        </IconButton>
      </div>
      <Collapse open={openNav}>
        {navList}
        <Button
          as={Link}
          to="/login"
          fullWidth
          variant="gradient"
          size="sm"
          onClick={() => setOpenNav(false)}
        >
          <span>Login</span>
        </Button>
      </Collapse>
    </Navbar>
  );
}
