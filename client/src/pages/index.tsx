import React, { useEffect, useState } from "react";
import ReactAudioPlayer from "react-audio-player";
import Image from "next/image";

interface Product {
  image: string;
  title: string;
  price: string;
  audio_file: string;
  status: string;
}

const Home = () => {
  const [searchInput, setSearchInput] = useState("");
  const [productDetails, setProduct] = useState<Product | undefined>();
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: { preventDefault: () => void }) => {
    e.preventDefault();

    setLoading(true);

    fetch("http://localhost:8080/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ keyword: searchInput }),
    })
      .then((response) => response.json())
      .then((data) => {
        setProduct(data);
        setLoading(false);
      })
      .catch((error) => {
        setLoading(false);
        console.error("Error fetching data:", error);
      });

    setSearchInput("");
  };
  console.log(productDetails?.image);
  return (
    <div className="flex flex-col text-center mt-40">
      <h1 className="font-bold font-mono tracking-wider">Product Search</h1>
      <form
        id="searchForm"
        onSubmit={handleSubmit}
        className="flex flex-col w-1/3 m-auto text-black mt-6"
      >
        <input
          required
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search a product"
          className="rounded-md p-3"
        />
        <button
          type="submit"
          className="bg-blue-500 hover.bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
        >
          Search
        </button>
      </form>
      {loading ? (
        <div className="flex justify-center mt-6">
          <p>Loading...</p>
        </div>
      ) : productDetails !== undefined ? (
        productDetails.status === "error" ? (
          <div className="flex justify-center mt-6">
            <p>No shopping ads found for {searchInput}</p>
          </div>
        ) : (
          <div className="mt-6 m-auto max-w-md rounded overflow-hidden shadow-lg border">
            <div className="flex">
              <div className="border-gray-400">
                <Image
                  src={productDetails.image}
                  alt={productDetails.title}
                  width={400}
                  height={600}
                />
              </div>
              <div className="font-bold text-xl mb-2 p-4">
                The price of {productDetails.title} is&nbsp;
                {productDetails.price}
                <ReactAudioPlayer
                  src={productDetails.audio_file}
                  autoPlay
                  controls
                />
              </div>
            </div>
          </div>
        )
      ) : null}
    </div>
  );
};

export default Home;
