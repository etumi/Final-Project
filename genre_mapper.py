def get_genre_prediction(prediction):

    genre_dict =  { 0: 'drama', 1: 'comedy', 2: 'action', 3: 'thriller', 4: 'adventure', 5: 'horror', 6: 'fantasy',7: 'crime',8: 'romance', 9: 'animation'}

    result = []
    y = prediction[0]
    for i in range(len(y)):
        if y[i] == 1:
            result.append(genre_dict[i])

    return {'response': result}
