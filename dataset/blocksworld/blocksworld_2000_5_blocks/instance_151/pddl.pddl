

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(ontable d)
(on e d)
(clear b)
(clear c)
)
(:goal
(and
(on a d)
(on b a)
(on c b)
(on e c))
)
)


