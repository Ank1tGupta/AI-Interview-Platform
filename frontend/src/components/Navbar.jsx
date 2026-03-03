import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FiMenu, FiX } from "react-icons/fi";

export default function Navbar() {
	const [open, setOpen] = useState(false);
	const navigate = useNavigate();

	return (
		<header className="bg-white shadow-sm">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div className="flex justify-between items-center h-16">
					<div className="flex items-center">
						<button
							onClick={() => setOpen(!open)}
							className="mr-3 inline-flex items-center justify-center p-2 rounded-md text-gray-600 sm:hidden"
							aria-label="Toggle menu"
						>
							{open ? <FiX size={20} /> : <FiMenu size={20} />}
						</button>

						<div className="text-lg font-semibold text-indigo-600 cursor-pointer" onClick={() => navigate('/') }>
							AI Interview
						</div>
					</div>

					<nav className="hidden sm:flex sm:space-x-6 text-gray-600">
						<Link to="/dashboard" className="hover:text-indigo-600">Dashboard</Link>
						<Link to="/interviews" className="hover:text-indigo-600">Interviews</Link>
					</nav>
				</div>
			</div>

			{open && (
				<div className="sm:hidden border-t">
					<div className="px-4 pt-2 pb-4 space-y-2">
						<Link to="/dashboard" className="block" onClick={() => setOpen(false)}>Dashboard</Link>
						<Link to="/interviews" className="block" onClick={() => setOpen(false)}>Interviews</Link>
					</div>
				</div>
			)}
		</header>
	);
}
