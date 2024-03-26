

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(ontable d)
(on e b)
(clear c)
(clear d)
)
(:goal
(and
(on b d)
(on c b)
(on d e))
)
)


