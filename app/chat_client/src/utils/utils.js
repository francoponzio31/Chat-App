export async function toBase64(file){
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result.split(',')[1])
        reader.onerror = error => reject(error)
    })
}


export function getUserPictureFilename(pictureId){
    return (
        pictureId ? `/files/${pictureId}` : "/circle-user-solid.svg"
    )
}


