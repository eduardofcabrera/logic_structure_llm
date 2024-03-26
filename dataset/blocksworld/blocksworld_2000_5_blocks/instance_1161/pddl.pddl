

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(ontable c)
(on d c)
(on e a)
(clear b)
)
(:goal
(and
(on c d)
(on d a)
(on e b))
)
)


