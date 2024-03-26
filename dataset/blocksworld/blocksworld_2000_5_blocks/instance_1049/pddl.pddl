

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(on d c)
(on e b)
(clear a)
(clear d)
)
(:goal
(and
(on b e)
(on c b)
(on d c)
(on e a))
)
)


