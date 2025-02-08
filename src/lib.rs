use poppy_filters::v2::BloomFilter;
use sha2::{Sha256, Digest};
use std::fs::File;
use std::io::{BufReader, Read};
use std::path::Path;

pub fn b3content(path: &std::path::Path) -> String {
    match std::fs::File::open(path) {
        Ok(mut file) => {
            let mut hasher = blake3::Hasher::new();
            let _temp = std::io::copy(&mut file, &mut hasher);
            let hash = hasher.finalize();
            hash.to_string()
        },
        Err(_) => "ERROR".to_string(),
    }
}

pub fn b3text(text: String) -> String {
    let mut hasher = blake3::Hasher::new();
    hasher.update(text.as_bytes());
    let hash = hasher.finalize();
    return hash.to_string()
}

pub fn b3unix(path: String) -> String {
    let out = path.split('/');
    let mut out = out.collect::<Vec<&str>>();
    if out.len() > 3 {
        if out[1] == "home" {
            out[2] = "user";
            let path = out.join("/");
            let hash = b3text(path);
            return hash.to_string();
        } else if out[1] == "Users" && out[2] != "Shared" {
            out[2] = "user";
            let path = out.join("/");
            let hash = b3text(path);
            return hash.to_string();
        } else {
            let hash = b3text(path);
            return hash.to_string();
        }
    } else {
        let hash = b3text(path);
        return hash.to_string();
    }
}

pub fn b3windows(path: String) -> String {
    let out = path.split('\\');
    let mut out = out.collect::<Vec<&str>>();
    if out.len() > 3 {
        if out[1] == "Users" && (out[2] != "Default" || out[2] != "Public") {
            out[2] = "user";
            let path = out.join("\\");
            let hash = b3text(path);
            return hash.to_string();
        } else {
            let hash = b3text(path);
            return hash.to_string();
        }
    } else {
        let hash = b3text(path);
        return hash.to_string();
    }
}

pub fn download() {
    let client = reqwest::blocking::Client::new();
    let release = client.get("https://api.github.com/repos/jblukach/artifacts/releases/latest")
        .header("User-Agent", "Artifacts Download (https://github.com/jblukach/artifacts/releases)")
        .send().unwrap();
    let json: serde_json::Value = release.json().unwrap();
    let assets = json["assets"].as_array().unwrap();
    for asset in assets {
        let url = asset["browser_download_url"].as_str().unwrap();
        println!("Download Link: {}", url);
        let filename = url.split("/").last().unwrap();
        let fullpath = std::env::current_exe().unwrap().parent().unwrap().join(filename);
        let response = client.get(url).send().unwrap();
        let mut file = std::fs::File::create(fullpath.clone()).unwrap();
        std::io::copy(&mut response.bytes().unwrap().as_ref(), &mut file).unwrap();
        println!("File Download: {}", fullpath.display());
    }
}

pub fn status() {
    let lolpath = std::env::current_exe().unwrap().parent().unwrap().join("lol.poppy");
    let mmipath = std::env::current_exe().unwrap().parent().unwrap().join("mmi.poppy");
    if Path::new(&lolpath).exists() && Path::new(&mmipath).exists() {
        let lolfile = File::open(&lolpath).unwrap();
        let lolpoppy = BloomFilter::from_reader(lolfile).unwrap();
        println!("Estimate: {} {}", lolpoppy.count_estimate(), lolpath.display());
        let mmifile = File::open(&mmipath).unwrap();
        let mmipoppy = BloomFilter::from_reader(mmifile).unwrap();
        println!("Estimate: {} {}", mmipoppy.count_estimate(), mmipath.display());
    } else {
        println!("Required File: {}", lolpath.display());
        println!("Required File: {}", mmipath.display());
        println!("Download Link: https://github.com/jblukach/artifacts/releases");
    }
}

fn verification(path: &Path) -> String {
    let file = File::open(path).unwrap();
    let mut reader = BufReader::new(file);
    let mut hasher = Sha256::new();
    let mut buffer = Vec::new();
    reader.read_to_end(&mut buffer).unwrap();
    hasher.update(&buffer);
    let result = hasher.finalize();
    let hash = format!("{:x}", result);
    return hash;
}

pub fn verify() {
    let lolpath = std::env::current_exe().unwrap().parent().unwrap().join("lol.poppy");
    let mmipath = std::env::current_exe().unwrap().parent().unwrap().join("mmi.poppy");
    let verifypath = std::env::current_exe().unwrap().parent().unwrap().join("verification.csv");
    if Path::new(&lolpath).exists() && Path::new(&mmipath).exists() && Path::new(&verifypath).exists() {
        let file = std::fs::File::open(verifypath.clone()).unwrap();
        let mut reader = csv::Reader::from_reader(file);
        let records = reader.records();
        for record in records {
            let record = record.unwrap();
            let hash = record.get(0).unwrap();
            let fname = record.get(1).unwrap();
            if fname == "lol.poppy" {
                let sha256 = verification(&lolpath);
                if sha256 == *hash {
                    println!("Verified: {}", lolpath.display());
                } else {
                    println!("Failure: {}", lolpath.display());
                }
            } else if fname == "mmi.poppy" {
                let sha256 = verification(&mmipath);
                if sha256 == *hash {
                    println!("Verified: {}", mmipath.display());
                } else {
                    println!("Failure: {}", mmipath.display());
                }
            }
        }
    } else {
        println!("Required File: {}", lolpath.display());
        println!("Required File: {}", mmipath.display());
        println!("Required File: {}", verifypath.display());
        println!("Download Link: https://github.com/jblukach/artifacts/releases");
    }
}